from __future__ import annotations

from collections import defaultdict
from typing import Literal
from typing import TypeAlias
from pydantic import BaseModel

COMMON_INSTRUCTIONS = (

    "You are Mosaed (مساعد), a quick and friendly Domino's Cashier Agent. \n"
    "You Can Speak arabic, english and indian , but you prefer to speak Arabic. \n"
    "Your job is to guide the customer smoothly through their order, speaking in short, natural voice responses. \n"
    "This is a voice interaction-assume the customer just pulled up and is speaking to you on tha cashier. \n"
    "Respond like you're hearing them, not reading text. \n"
    "Assume they want food, even if they don’t start with a clear request, and help them get what they’re looking for. \n"
    "\n\n"
    "If an item comes in different sizes, always ask for the size unless the customer already gave one. \n"
    "\n\n"
    "Be fast-keep responses short and snappy. \n"
    "Sound human-sprinkle in light vocal pauses like 'Mmh…', 'Let me see…', or 'Alright…' at natural moments-but not too often. \n"
    "Keep everything upbeat and easy to follow. Never overwhelm the customer, don't ask multiple questions at the same time. \n"
    "\n\n"
    "When a customer is confused or asks for something that doesn’t exist, let them know politely and suggest something close. \n"
    "Always confirm what they picked in a warm, clear way, like: 'Alright, one medium pepproni pizza!' \n"
    "If something’s unavailable, say so with empathy: 'Ah, we're out of Sweet Tea right now-can I get you a Coke instead?' \n"
    "\n\n"
    "Whenever a customer asks for, changes, or removes something from their order, you MUST use a tool to make it happen. \n"
    "If the customer want to edit an item, you must remove the previous version before adding the new one. \n"
    "Don’t fake it. Don’t pretend something was added - actually **call** the tool and make it real on the ordering system. \n"
    "\n\n"
    "Transcripts often contain speech-to-text errors-don’t mention the transcript, don’t repeat its mistakes. \n"
    "Instead treat each user input as a rough draft of what was said. \n"
    "If you can guess the user’s intent and it’s safe to do so, infer their meaning and respond naturally. \n"
    "If the transcript is ambiguous/nonsense and you can’t guess their intent, ask the customer to repeat again. \n"
    "Stay on-topic; if input is nonsensical, ask for concise clarification. \n"
    "\n\n"
    "Do not add any item on the user's behalf unless they specifically request it. If the user hasn't asked for an item, NEVER add it. \n"
    "\n\n"
    "When a customer changes an item, make sure to remove the previous version before adding the new one. \n"
    "Otherwise, the order may contain duplicates. \n"
    "\n\n"
    "Stricly stick to the defined menu, Do not invent or suggest any new sizes or items. \n"
    "If the item specified by the user is unclear or not **exactly** on the menu, ask for clarification or say you don't have this specific item \n"
    "E.g: a pizza isn't a Margherita  \n"
    "Do not ask for size unless the item has more than one size option specified. \n"
    "If an item does not require a size according to the menu, **NEVER** ask the customer to choose one or mention size at all. \n"
     "\n\n"
     "you should only use the id's of the items when adding them to the order,dont invent any new id's"
     "\n\n"
     "You should list the user order at the end of the conversation, and ask the user if they want to add anything else. \n"
     "\n\n"
     "AED when translated to arabic is درهم, and when translated to english is Dirham. \n"
     "S is small , M is medium, L is large. \n"
)


# ItemSize = Literal["S", "M", "L"]
ItemSize: TypeAlias = str

ItemCategory = Literal["drink", "pizza", "sauce", "chicken", "sides", "desserts"]


class MenuItem(BaseModel):
    id: str
    name: str
    price: float
    ingredients: str | None = None
    available: bool
    size: ItemSize | None = None
    voice_alias: str | None = None
    category: ItemCategory


class FakeDB:
    async def list_drinks(self) -> list[MenuItem]:
        drink_data = [
            {
                "id": "pepsi",
                "name": "Pepsi",
                "sizes": {
                    "Can": {"price": 5},
                    "Bottle (2.27L)": {"price": 14},
                },
            },
            {
                "id": "pepsi_diet",
                "name": "Pepsi Diet",
                "sizes": {
                    "Can": {"price": 5},
                    "Bottle (2.27L)": {"price": 14},
                },
            },
            {
                "id": "miranda",
                "name": "Miranda",
                "sizes": {
                    "Can": {"price": 5},
                    "Bottle (2.27L)": {"price": 14},
                },
            },
            {
                "id": "seven_up",
                "name": "7UP",
                "sizes": {
                    "Can": {"price": 5},
                    "Bottle (2.27L)": {"price": 14},
                },
            },
            {
                "id": "water",
                "name": "Water (500ml)",
                "price": 4,
            },
        ]

        items = []
        for item in drink_data:
            if sizes := item.get("sizes", {}):
                for size, size_details in sizes.items():
                    items.append(
                        MenuItem(
                            id=item["id"],
                            name=item["name"],
                            price=size_details["price"],
                            size=size,
                            available=True,
                            category="drink",
                        )
                    )
            else:
                items.append(
                    MenuItem(
                        id=item["id"],
                        name=item["name"],
                        price=item["price"],
                        available=True,
                        category="drink",
                    )
                )

        return items

    async def list_pizza(self) -> list[MenuItem]:
        raw_items = [
            {
                "id": "margherita",
                "name": "Margherita",
                "ingredients": "Signature Pizza Sauce and Mozzarella Cheese.",
                "sizes": {
                    "S": {"price": 26},
                    "M": {"price": 42},
                    "L": {"price": 56},
                },
            },
            {
                "id": "veggie",
                "name": "Veggie",
                "ingredients": "Green Peppers, Onions, Mushrooms, Black Olives, Mozzarella & Signature Pizza Sauce.",
                "sizes": {
                    "S": {"price": 28},
                    "M": {"price": 44},
                    "L": {"price": 60},
                },
            },
            {
                "id": "ultimate_pepperoni",
                "name": "Ultimate Pepperoni",
                "ingredients": "Beef Pepperoni, Mozzarella & Signature Pizza Sauce.",
                "sizes": {
                    "S": {"price": 28},
                    "M": {"price": 44},
                    "L": {"price": 60},
                },
            },
            {
                "id": "mexican_green_wave",
                "name": "Mexican Green Wave",
                "ingredients": "Crunchy Onion, Crisp Capsicum and Jalapeno with Italian Herbs & Signature Pizza Sauce.",
                "sizes": {
                    "S": {"price": 28},
                    "M": {"price": 44},
                    "L": {"price": 60},
                },
            },
            {
                "id": "hawaiian",
                "name": "Hawaiian",
                "ingredients": "Beef Pepperoni, Hawaiian Pineapple, Mozzarella & Signature Pizza Sauce.",
                "sizes": {
                    "S": {"price": 28},
                    "M": {"price": 44},
                    "L": {"price": 60},
                },
            },
            {
                "id": "chicken_legend",
                "name": "Chicken Legend",
                "ingredients": "Grilled Chicken breast, Onions, Mozzarella, American cheese, Oregano. Choose your sauce: Ranch, BBQ, or Hot Sauce.",
                "sizes": {
                    "S": {"price": 28},
                    "M": {"price": 44},
                    "L": {"price": 60},
                },
            },
            {
                "id": "meatzza",
                "name": "Meatzza",
                "ingredients": "Beef pepperoni, Italian sausage, beef and Signature Pizza Sauce.",
                "sizes": {
                    "S": {"price": 28},
                    "M": {"price": 44},
                    "L": {"price": 60},
                },
            },
            {
                "id": "chicken_memphis_bbq",
                "name": "Chicken Memphis BBQ",
                "ingredients": "Grilled chicken, BBQ sauce, green peppers and onion.",
                "sizes": {
                    "S": {"price": 28},
                    "M": {"price": 44},
                    "L": {"price": 60},
                },
            },
            {
                "id": "italiano",
                "name": "Italiano",
                "ingredients": "Beef Pepperoni, Mushrooms, Italian Sausage, Mozzarella & Signature Pizza Sauce.",
                "sizes": {
                    "S": {"price": 28},
                    "M": {"price": 44},
                    "L": {"price": 60},
                },
            },
            {
                "id": "tex_mex",
                "name": "Tex-Mex",
                "ingredients": "Grilled Chicken breast, Topped with Onions, Black Olives, Green Peppers, Mozzarella & Signature Pizza Sauce. Spice It Up with Jalapeno.",
                "sizes": {
                    "S": {"price": 28},
                    "M": {"price": 44},
                    "L": {"price": 60},
                },
            },
            {
                "id": "hot_and_spicy",
                "name": "Hot & Spicy",
                "ingredients": "Beef, Onions, Green Pepper, Jalapenos, Mozzarella & Signature Tomato Sauce.",
                "sizes": {
                    "S": {"price": 28},
                    "M": {"price": 44},
                    "L": {"price": 60},
                },
            },
            {
                "id": "chicken_kickers",
                "name": "Chicken Kickers",
                "ingredients": "American Cheese, Chicken Kickers, Jalapeno, mozzarella, Oregano with Honey Mustard sauce.",
                "sizes": {
                    "S": {"price": 30},
                    "M": {"price": 48},
                    "L": {"price": 64},
                },
            },
            {
                "id": "paneer_tikka",
                "name": "Paneer Tikka",
                "ingredients": "Fresh Paneer Tikka, red & green pepper, Onion, mozzarella and signature pizza sauce topped with mint drizzle.",
                "sizes": {
                    "M": {"price": 48},
                    "L": {"price": 64},
                },
            },
            {
                "id": "chicken_tikka",
                "name": "Chicken Tikka",
                "ingredients": "Succulent baked Chicken Tikka with red & green pepper, Onion, mozzarella and signature pizza sauce topped with mint drizzle.",
                "sizes": {
                    "M": {"price": 48},
                    "L": {"price": 64},
                },
            },
            {
                "id": "four_cheese",
                "name": "Four Cheese",
                "ingredients": "A combination of mozzarella, Feta cheese, American cheese and rich creamy cheese along with our signature Pizza sauce; sprinkled with oregano.",
                "sizes": {
                    "S": {"price": 30},
                    "M": {"price": 48},
                    "L": {"price": 64},
                },
            },
            {
                "id": "extravaganzza",
                "name": "Extravaganzza",
                "ingredients": "Beef Pepperoni, Italian Sausage, Beef, Onions, Green Peppers, Mushrooms, Black Olives, Mozzarella & Signature Pizza Sauce.",
                "sizes": {
                    "S": {"price": 30},
                    "M": {"price": 48},
                    "L": {"price": 64},
                },
            },
            {
                "id": "veggie_legend_jalapenos",
                "name": "Veggie Legend & Jalapenos",
                "ingredients": "Onions, Red Pepper, Black Olives, mozzarella, Jalapenos & slice of american cheese with ranch sauce. (Ranch Sauce contains eggs).",
                "sizes": {
                    "S": {"price": 30},
                    "M": {"price": 48},
                    "L": {"price": 64},
                },
            },
            {
                "id": "chicken_legend_ranch_jalapenos",
                "name": "Chicken Legend Ranch & Jalapenos",
                "ingredients": "Grilled Chicken, Onions, Mozzarella, slice of American cheese, Jalapenos, Oregano & Ranch Sauce.",
                "sizes": {
                    "S": {"price": 30},
                    "M": {"price": 48},
                    "L": {"price": 64},
                },
            },
            {
                "id": "philly_cheese_steak",
                "name": "Philly Cheese Steak",
                "ingredients": "Slices of Beef Steak, Onions, Green Peppers, Mushroom, Mozzarella, slice of American cheese. Add Dynamite Sauce for Extra Spice.",
                "sizes": {
                    "S": {"price": 30},
                    "M": {"price": 48},
                    "L": {"price": 64},
                },
            },
            {
                "id": "chicken_alfredo",
                "name": "Chicken Alfredo",
                "ingredients": "Grilled Chicken with Fresh Mushroom and Original Alfredo Sauce.",
                "sizes": {
                    "S": {"price": 30},
                    "M": {"price": 48},
                    "L": {"price": 64},
                },
            },
            {
                "id": "dynamite_chicken",
                "name": "Dynamite Chicken",
                "ingredients": "Baked Chicken, Onion, Green Peppers, Mozzarella, slice of American Cheese, Oregano, Dynamite Sauce. Add Hot Sauce for Extra Spice.",
                "sizes": {
                    "S": {"price": 30},
                    "M": {"price": 48},
                    "L": {"price": 64},
                },
            },
            {
                "id": "chicken_feast",
                "name": "Chicken Feast",
                "ingredients": "Loaded with a delicious combination of grilled chicken, famous chicken kickers and premium chicken, spicing it up with jalapeno and red pepper slices.",
                "sizes": {
                    "S": {"price": 30},
                    "M": {"price": 48},
                    "L": {"price": 64},
                },
            },
        ]

        items = []
        for item in raw_items:
            if sizes := item.get("sizes", {}):
                for size, size_details in sizes.items():
                    items.append(
                        MenuItem(
                            id=item["id"],
                            name=item["name"],
                            ingredients=item["ingredients"],
                            price=size_details["price"],
                            size=size,
                            available=True,
                            category="pizza",
                        )
                    )
            else:
                items.append(
                    MenuItem(
                        id=item["id"],
                        name=item["name"],
                        ingredients=item["ingredients"],
                        price=item["price"],
                        available=True,
                        category="pizza",
                    )
                )

        return items

    async def list_chicken(self) -> list[MenuItem]:
        raw_items = [
            {
                "id": "chicken_wings",
                "name": "Chicken Wings",
                "ingredients": "Served with your choice of Hot, BBQ, or Ranch sauce.",
                "sizes": {
                    "8 Pieces": {"price": 25},
                    "10 Pieces": {"price": 30},
                },
            },
            {
                "id": "chicken_kickers_item",
                "name": "Chicken Kickers",
                "ingredients": "Baked chicken breast with a hint of Buffalo flavor, served with your choice of sauces.",
                "sizes": {
                    "8 Pieces": {"price": 25},
                    "10 Pieces": {"price": 30},
                },
            },
            {
                "id": "dynamite_chicken_item",
                "name": "Dynamite Chicken",
                "ingredients": "Baked chicken breast topped with Dynamite sauce.",
                "sizes": {
                    "20 Pieces": {"price": 25},
                },
            },
            {
                "id": "premium_chicken",
                "name": "Premium Chicken",
                "ingredients": "Choose your flavor: Spicy Jalapeno & Pineapple or Classic Hot Buffalo.",
                "sizes": {
                    "12 Pieces": {"price": 25},
                },
            },
        ]

        items = []
        for item in raw_items:
            if sizes := item.get("sizes", {}):
                for size, size_details in sizes.items():
                    items.append(
                        MenuItem(
                            id=item["id"],
                            name=item["name"],
                            ingredients=item["ingredients"],
                            price=size_details["price"],
                            size=size,
                            available=True,
                            category="chicken",
                        )
                    )
            else:
                items.append(
                    MenuItem(
                        id=item["id"],
                        name=item["name"],
                        ingredients=item.get("ingredients"),
                        price=item["price"],
                        available=True,
                        category="chicken",
                    )
                )
        return items

    async def list_sides(self) -> list[MenuItem]:
        raw_items = [
            {
                "id": "stuffed_cheesy_bread_fajita",
                "name": "Stuffed Cheesy Bread (Fajita)",
                "ingredients": "Stuffed with Mozzarella, Grilled Chicken Breast & Jalapeno. Served with Marinara Sauce.",
                "sizes": {
                    "8 Pieces": {"price": 25},
                },
            },
            {
                "id": "stuffed_cheesy_bread_italiano",
                "name": "Stuffed Cheesy Bread (Italiano)",
                "ingredients": "Stuffed with Mozzarella, Beef Pepperoni, Jalapeno, Peppers & Onions. Served with Marinara Sauce.",
                "sizes": {
                    "8 Pieces": {"price": 25},
                },
            },
            {
                "id": "stuffed_cheesy_bread_mozzarella",
                "name": "Stuffed Cheesy Bread (Mozzarella)",
                "ingredients": "Stuffed with Mozzarella. Served with Marinara Sauce.",
                "sizes": {
                    "8 Pieces": {"price": 25},
                },
            },
            {
                "id": "garlic_twists",
                "name": "Garlic Twists",
                "ingredients": "Garlic Twists served with marinara sauce.",
                "sizes": {
                    "8 Pieces": {"price": 20},
                },
            },
            {
                "id": "philly_steak_wedges",
                "name": "Philly Steak Wedges",
                "ingredients": "Potato Wedges, Mozzarella, Slices of Beef Steak, Onions, Jalapeno with Dynamite Sauce.",
                "price": 22,
            },
            {
                "id": "beef_wedges",
                "name": "Beef Wedges",
                "ingredients": "Potato Wedges, Mozzarella, Beef, Onions, Jalapeno with Dynamite Sauce.",
                "price": 22,
            },
            {
                "id": "tikka_wedges",
                "name": "Tikka Wedges",
                "ingredients": "Potato Wedges, Mozzarella, Chicken Tikka, Onions, and Peppers with Hot Buffalo & Ranch Sauces.",
                "price": 22,
            },
            {
                "id": "kickers_wedges",
                "name": "Kickers Wedges",
                "ingredients": "Potato Wedges, Mozzarella, Chicken Kickers, Onions, and Peppers with Hot Buffalo & Ranch Sauces.",
                "price": 22,
            },
            {
                "id": "veggie_wedges",
                "name": "Veggie Wedges",
                "ingredients": "Potato Wedges, Mozzarella, Green Peppers, Red Peppers, and Jalapeno served with Hot Buffalo & Ranch Sauces.",
                "price": 22,
            },
        ]

        items = []
        for item in raw_items:
            if sizes := item.get("sizes", {}):
                for size, size_details in sizes.items():
                    items.append(
                        MenuItem(
                            id=item["id"],
                            name=item["name"],
                            ingredients=item["ingredients"],
                            price=size_details["price"],
                            size=size,
                            available=True,
                            category="sides",
                        )
                    )
            else:
                items.append(
                    MenuItem(
                        id=item["id"],
                        name=item["name"],
                        ingredients=item.get("ingredients"),
                        price=item["price"],
                        available=True,
                        category="sides",
                    )
                )
        return items

    async def list_desserts(self) -> list[MenuItem]:
        raw_items = [
            {
                "id": "chocolate_lava_cake",
                "name": "Chocolate Lava Cake",
                "ingredients": "Oven baked chocolate cake with molten chocolate fudge on the inside.",
                "sizes": {
                    "1 Piece": {"price": 12},
                    "2 Pieces": {"price": 22},
                },
            },
            {
                "id": "cinnamon_twist",
                "name": "Cinnamon Twist",
                "ingredients": "Baked pan dough, drizzled with cinnamon, served with sweet icing.",
                "sizes": {
                    "8 Pieces": {"price": 20},
                },
            },
            {
                "id": "crownies",
                "name": "Crownies",
                "ingredients": "A fresh baked fudge brownie mixed with milk chocolate chunk cookies, cut into squares.",
                "sizes": {
                    "9 Pieces": {"price": 25},
                },
            },
        ]
        
        items = []
        for item in raw_items:
            if sizes := item.get("sizes", {}):
                for size, size_details in sizes.items():
                    items.append(
                        MenuItem(
                            id=item["id"],
                            name=item["name"],
                            ingredients=item["ingredients"],
                            price=size_details["price"],
                            size=size,
                            available=True,
                            category="desserts",
                        )
                    )
            else:
                items.append(
                    MenuItem(
                        id=item["id"],
                        name=item["name"],
                        ingredients=item.get("ingredients"),
                        price=item["price"],
                        available=True,
                        category="desserts",
                    )
                )
        return items

    async def list_sauces(self) -> list[MenuItem]:
        raw_items = [
            {"id": "ranch_sauce", "name": "Ranch Sauce", "price": 3},
            {"id": "marinara_sauce", "name": "Marinara Sauce", "price": 3},
            {"id": "sweet_icing_sauce", "name": "Sweet Icing Sauce", "price": 3},
            {"id": "bbq_sauce", "name": "BBQ Sauce", "price": 3},
            {"id": "hot_sauce", "name": "Hot Sauce", "price": 3},
        ]
        
        items = []
        for item in raw_items:
            if sizes := item.get("sizes", {}):
                for size, size_details in sizes.items():
                    items.append(
                        MenuItem(
                            id=item["id"],
                            name=item["name"],
                            ingredients=item.get("ingredients"), # Safely gets ingredients (None here)
                            price=size_details["price"],
                            size=size,
                            available=True,
                            category="sauce",
                        )
                    )
            else:
                items.append(
                    MenuItem(
                        id=item["id"],
                        name=item["name"],
                        ingredients=item.get("ingredients"), # Safely gets ingredients (None here)
                        price=item["price"],
                        available=True,
                        category="sauce",
                    )
                )
        return items
# The code below is optimized for ease of use instead of efficiency.


def map_by_sizes(
    items: list[MenuItem],
) -> tuple[dict[str, dict[ItemSize, MenuItem]], list[MenuItem]]:
    result = defaultdict(dict)
    leftovers = [item for item in items if not item.size]
    [result[item.id].update({item.size: item}) for item in items if item.size]
    return dict(result), leftovers


def find_items_by_id(
    items: list[MenuItem], item_id: str, size: ItemSize | None = None
) -> list[MenuItem]:
    return [item for item in items if item.id == item_id and (size is None or item.size == size)]


def _generate_menu_text(title: str, items: list[MenuItem]) -> str:
    """
    Generates a formatted string for a list of menu items using a
    structured, YAML-like key-value format.
    """
    menu_lines = []
    items_with_sizes, items_without_sizes = map_by_sizes(items)

    # --- Part 1: Process items that have different sizes ---
    for _, size_map in items_with_sizes.items():
        # Get a sample item to access shared info like name and ingredients
        first_item = next(iter(size_map.values()))
        
        # Use a consistent, indented key-value format
        menu_lines.append(f"  - name: {first_item.name}")
        menu_lines.append(f"    id: {first_item.id}")
        if first_item.ingredients:
            menu_lines.append(f"    ingredients: {first_item.ingredients}")
        
        menu_lines.append("    sizes:")
        for size, item in size_map.items():
            # Format each size as a list item with a key (size) and value (price)
            size_line = f'      - "{size}": AED {item.price:.2f}'
            if not item.available:
                # Add availability on a new, more indented line for clarity
                menu_lines.append(size_line)
                menu_lines.append("        available: false")
            else:
                menu_lines.append(size_line)

    # --- Part 2: Process items that do not have selectable sizes ---
    for item in items_without_sizes:
        # Use the same consistent key-value format
        menu_lines.append(f"  - name: {item.name}")
        menu_lines.append(f"    id: {item.id}")
        menu_lines.append(f"    price: AED {item.price:.2f}")
        if item.ingredients:
            menu_lines.append(f"    ingredients: {item.ingredients}")
        
        menu_lines.append("    size_info: Not size-selectable")

        # Add an explicit availability key if the item is unavailable
        if not item.available:
            menu_lines.append("    available: false")

    return f"# {title}:\n" + "\n".join(menu_lines)

def menu_instructions(category: ItemCategory, *, items: list[MenuItem]) -> str:
    """
    Acts as a router to generate the correct menu instructions for a given category.
    """
    category_titles = {
        "pizza": "Pizzas",
        "chicken": "Chicken",
        "drink": "Drinks",
        "sides": "Sides",
        "desserts": "Desserts",
        "sauce": "Sauces",
    }
    
    title = category_titles.get(category, category.capitalize())
    return _generate_menu_text(title, items)


# def menu_instructions2(category: ItemCategory, *, items: list[MenuItem]) -> str:
#     if category == "drink":
#         return _drink_menu_instructions(items)
#     elif category == "chicken":
#         return _chicken_menu_instructions(items)
#     elif category == "sides":
#         return _sides_menu_instructions(items)
#     elif category == "sauce":
#         return _sauce_menu_instructions(items)
#     elif category == "pizza":
#         return _pizza_menu_instructions(items)
#     elif category == "desserts":
#         return _desserts_menu_instructions(items)


# def _drink_menu_instructions(items: list[MenuItem]) -> str:
#     available_sizes, leftovers = map_by_sizes(items)
#     menu_lines = []

#     for _, size_map in available_sizes.items():
#         first_item = next(iter(size_map.values()))
#         menu_lines.append(f"  - {first_item.name} (id:{first_item.id}):")

#         for item in size_map.values():
#             line = f" - Size {item.size}, AED{item.price:.2f}"
#             if not item.available:
#                 line += " UNAVAILABLE"
#             menu_lines.append(line)

#     for item in leftovers:
#         # explicitely saying there is no `size` for this item, otherwise the LLM seems to hallucinate quite often
#         line = f"  - {item.name}, AED {item.price:.2f} (id:{item.id}) - Not size-selectable`"
#         if not item.available:
#             line += " UNAVAILABLE"
#         menu_lines.append(line)

#     return "# Drinks:\n" + "\n".join(menu_lines)



# def _sauce_menu_instructions(items: list[MenuItem]) -> str:
#     menu_lines = []
#     for item in items:
#         line = f"  - {item.name} , AED {item.price:.2f} (id:{item.id})"
#         if not item.available:
#             line += " UNAVAILABLE"
#         menu_lines.append(line)

#     return "# Sauces:\n" + "\n".join(menu_lines)


# # regular/a la carte
# def _pizza_menu_instructions(items: list[MenuItem]) -> str:
#     available_sizes, leftovers = map_by_sizes(items)
#     menu_lines = []

#     for _, size_map in available_sizes.items():
#         first_item = next(iter(size_map.values()))
#         menu_lines.append(f"  - {first_item.name} (id:{first_item.id}) , ingredients ({first_item.ingredients}):")

#         for item in size_map.values():
#             line = f"    - Size {item.size}, AED{item.price:.2f}"
#             if not item.available:
#                 line += " UNAVAILABLE"
#             menu_lines.append(line)

#     for item in leftovers:
#         line = f"  - {item.name}, AED{item.price:.2f} (id:{item.id}) - Not size-selectable"
#         if not item.available:
#             line += " UNAVAILABLE"
#         menu_lines.append(line)

#     return "# pizza items/À la carte:\n" + "\n".join(menu_lines)

# def _chicken_menu_instructions(items: list[MenuItem]) -> str:
#     available_sizes, leftovers = map_by_sizes(items)
#     menu_lines = []

#     for _, size_map in available_sizes.items():
#         first_item = next(iter(size_map.values()))
#         menu_lines.append(f"  - {first_item.name} (id:{first_item.id}) , ingredients ({first_item.ingredients}):")

#         for item in size_map.values():
#             line = f"    - Size {item.size}, AED{item.price:.2f}"
#             if not item.available:
#                 line += " UNAVAILABLE"
#             menu_lines.append(line)

#     for item in leftovers:
#         line = f"  - {item.name}, AED{item.price:.2f} (id:{item.id}) - Not size-selectable"
#         if not item.available:
#             line += " UNAVAILABLE"
#         menu_lines.append(line)

#     return "# Chicken items:\n" + "\n".join(menu_lines)

# def _sides_menu_instructions(items: list[MenuItem]) -> str:
#     available_sizes, leftovers = map_by_sizes(items)
#     menu_lines = []

#     # --- Correctly handle items WITH sizes ---
#     for _, size_map in available_sizes.items():
#         first_item = next(iter(size_map.values()))
        
#         # Build the main line with name, ID, and ingredients
#         main_line = f"  - {first_item.name} (id: {first_item.id})"
#         if first_item.ingredients:
#             main_line += f", ingredients: {first_item.ingredients}"
#         menu_lines.append(main_line)
        
#         # Loop through each size and list its price
#         for item in size_map.values():
#             line = f"    - Size: {item.size}, AED {item.price:.2f}"
#             if not item.available:
#                 line += " (UNAVAILABLE)"
#             menu_lines.append(line)

#     # --- Correctly handle items WITHOUT sizes ---
#     for item in leftovers:
#         line = f"  - {item.name} (id: {item.id}), AED {item.price:.2f}"
#         if item.ingredients:
#             line += f", ingredients: {item.ingredients}"
#         line += " - Not size-selectable"
#         if not item.available:
#             line += " (UNAVAILABLE)"
#         menu_lines.append(line)

#     return "# Sides:\n" + "\n".join(menu_lines)


# def _desserts_menu_instructions(items: list[MenuItem]) -> str:
#     available_sizes, leftovers = map_by_sizes(items)
#     menu_lines = []

#     # --- Correctly handle items WITH sizes ---
#     for _, size_map in available_sizes.items():
#         first_item = next(iter(size_map.values()))
        
#         # Build the main line with name, ID, and ingredients
#         main_line = f"  - {first_item.name} (id: {first_item.id})"
#         if first_item.ingredients:
#             main_line += f", ingredients: {first_item.ingredients}"
#         menu_lines.append(main_line)

#         # Loop through each size and list its price
#         for item in size_map.values():
#             line = f"    - Size: {item.size}, AED {item.price:.2f}"
#             if not item.available:
#                 line += " (UNAVAILABLE)"
#             menu_lines.append(line)

#     # --- Correctly handle items WITHOUT sizes ---
#     for item in leftovers:
#         line = f"  - {item.name} (id: {item.id}), AED {item.price:.2f}"
#         if item.ingredients:
#             line += f", ingredients: {item.ingredients}"
#         line += " - Not size-selectable"
#         if not item.available:
#             line += " (UNAVAILABLE)"
#         menu_lines.append(line)

#     return "# Desserts:\n" + "\n".join(menu_lines)

