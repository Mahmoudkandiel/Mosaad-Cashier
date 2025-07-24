import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dataclasses import dataclass
from typing import Annotated

from database import (
    COMMON_INSTRUCTIONS,
    FakeDB,
    MenuItem,
    find_items_by_id,
    menu_instructions,
)
from dotenv import load_dotenv
from recipt_state import OrderedRegular, OrderState
from pydantic import Field

from livekit.agents import (
    Agent,
    AgentSession,
    AudioConfig,
    BackgroundAudioPlayer,
    FunctionTool,
    JobContext,
    RunContext,
    ToolError,
    WorkerOptions,
    cli,
    function_tool,
    # RoomInputOptions,
)
from livekit.plugins import  openai
from openai.types.beta.realtime.session import TurnDetection

load_dotenv()


@dataclass
class Userdata:
    #["drink", "pizza", "sauce", "chicken", "side", "dessert"]
    order: OrderState
    drink_items: list[MenuItem]
    pizza_items: list[MenuItem]
    sauce_items: list[MenuItem]
    dessert_items: list[MenuItem]
    side_items: list[MenuItem]
    chicken_items: list[MenuItem]




class DriveThruAgent(Agent):
    def __init__(self, *, userdata: Userdata) -> None:
        instructions = (
            COMMON_INSTRUCTIONS
            + "\n\n"
            + menu_instructions("drink", items=userdata.drink_items)
            + "\n\n"
            + menu_instructions("pizza", items=userdata.pizza_items)
            + "\n\n"
            + menu_instructions("sauce", items=userdata.sauce_items)
            + "\n\n"
            + menu_instructions("desserts", items=userdata.dessert_items)
            + "\n\n"
            + menu_instructions("sides", items=userdata.side_items)
            + "\n\n"
            + menu_instructions("chicken", items=userdata.chicken_items)
            + "\n\n"
        )
        print(instructions)

        super().__init__(
            instructions=instructions,
            tools=[
                self.build_regular_order_tool(
                    userdata.pizza_items, 
                    userdata.drink_items, 
                    userdata.sauce_items,
                    userdata.chicken_items,
                    userdata.side_items, 
                    userdata.dessert_items,
                ),
            ],
        )

    def build_regular_order_tool(
        self,
        pizza_items: list[MenuItem],
        drink_items: list[MenuItem],
        sauce_items: list[MenuItem],
        chicken_items: list[MenuItem],
        side_items: list[MenuItem],
        dessert_items: list[MenuItem],
    ) -> FunctionTool:
        all_items = pizza_items + drink_items + sauce_items + chicken_items + side_items + dessert_items
        available_ids = {item.id for item in all_items}

        @function_tool
        async def order_regular_item(
            ctx: RunContext[Userdata],
            item_id: Annotated[
                str,
                Field(
                    description="The ID of the item the user requested.",
                    json_schema_extra={"enum": list(available_ids)},
                ),
            ],
            size: Annotated[
                str | None, # Use a flexible string type
                Field(description="Size of the item, if applicable (e.g., 'S', 'Can', '8 Pieces'). Should be null if not specified or not applicable."),
            ] = None, 
        ) -> str:
            """
            Call this when the user orders **a single item on its own**

            The customer must provide clear and specific input. For example, item variants such as flavor must **always** be explicitly stated.

            The user might say—for example:
            - “Just the cheeseburger, no meal”
            - “A medium Coke”
            - “Can I get some ketchup?”
            - “Can I get a McFlurry Oreo?”
            """
            item_sizes = find_items_by_id(all_items, item_id)
            if not item_sizes:
                raise ToolError(f"error: {item_id} was not found.")

            if size == "null":
                size = None

            available_sizes = list({item.size for item in item_sizes if item.size})
            if size is None and len(available_sizes) > 1:
                raise ToolError(
                    f"error: {item_id} comes with multiple sizes: {', '.join(available_sizes)}. "
                    "Please clarify which size should be selected."
                )

            if size is not None and not available_sizes:
                size = None
                # raise ToolError(
                #     f"error: size should not be specified for item {item_id} as it does not support sizing options."
                # )

            if (size and available_sizes) and size not in available_sizes:
                raise ToolError(
                    f"error: unknown size {size} for {item_id}. Available sizes: {', '.join(available_sizes)}."
                )

            item = OrderedRegular(item_id=item_id, size=size)
            await ctx.userdata.order.add(item)
            return f"The item was added: {item.model_dump_json()}"

        return order_regular_item

    @function_tool
    async def remove_order_item(
        self,
        ctx: RunContext[Userdata],
        order_id: Annotated[
            list[str],
            Field(
                description="A list of internal `order_id`s of the items to remove. Use `list_order_items` to look it up if needed."
            ),
        ],
    ) -> str:
        """
        Removes one or more items from the user's order using their `order_id`s.

        Useful when the user asks to cancel or delete existing items (e.g., “Remove the cheeseburger”).

        If the `order_id`s are unknown, call `list_order_items` first to retrieve them.
        """
        not_found = [oid for oid in order_id if oid not in ctx.userdata.order.items]
        if not_found:
            raise ToolError(f"error: no item(s) found with order_id(s): {', '.join(not_found)}")

        removed_items = [await ctx.userdata.order.remove(oid) for oid in order_id]
        return "Removed items:\n" + "\n".join(item.model_dump_json() for item in removed_items)

    @function_tool
    async def list_order_items(self, ctx: RunContext[Userdata]) -> str:
        """
        Retrieves the current list of items in the user's order, including each item's internal `order_id`.

        Helpful when:
        - An `order_id` is required before modifying or removing an existing item.
        - Confirming details or contents of the current order.

        Examples:
        - User requests modifying an item, but the item's `order_id` is unknown (e.g., "Change the fries from small to large").
        - User requests removing an item, but the item's `order_id` is unknown (e.g., "Remove the cheeseburger").
        - User asks about current order details (e.g., "What's in my order so far?").
        """
        items = ctx.userdata.order.items.values()
        if not items:
            return "The order is empty"

        return "\n".join(item.model_dump_json() for item in items)


async def new_userdata() -> Userdata:
    fake_db = FakeDB()
    drink_items = await fake_db.list_drinks()
    pizza_items = await fake_db.list_pizza()
    sauce_items = await fake_db.list_sauces()
    chicken_items = await fake_db.list_chicken()
    side_items = await fake_db.list_sides()
    dessert_items = await fake_db.list_desserts()


    order_state = OrderState(items={})
    userdata = Userdata(
        order=order_state,
        drink_items=drink_items,
        pizza_items=pizza_items,
        sauce_items=sauce_items,
        chicken_items=chicken_items,
        side_items=side_items,
        dessert_items=dessert_items,
    )
    return userdata


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    userdata = await new_userdata()
    session = AgentSession[Userdata](
         userdata=userdata,
        llm = openai.realtime.RealtimeModel.with_azure(
        azure_deployment="gpt-4o-mini-realtime-preview",
        azure_endpoint="wss://naseh.openai.azure.com/",
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-10-01-preview",
        turn_detection=None,
        # tracing=False,
        ),
        turn_detection=TurnDetection(
            type="server_vad",
            threshold=0.5,
            prefix_padding_ms=300,
            silence_duration_ms=500,
            create_response=True,
            interrupt_response=True,
        ),
        # turn_detection="vad", # or EnglishModel()
        # vad=silero.VAD.load(),
    )

    background_audio = BackgroundAudioPlayer(
        ambient_sound=AudioConfig(
            str(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bg_noise.mp3")),
            volume=1.0,
        ),
    )

    await session.start(
        agent=DriveThruAgent(userdata=userdata), 
        room=ctx.room,
        # room_input_options=RoomInputOptions(
        #     # LiveKit Cloud enhanced noise cancellation
        #     # - If self-hosting, omit this parameter
        #     # - For telephony applications, use `BVCTelephony` for best results
        #     noise_cancellation=noise_cancellation.BVC(),
        # ),
    )
    await background_audio.start(room=ctx.room, agent_session=session)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))