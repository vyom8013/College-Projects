# menu_module.py

# Menu items organized by category
MENU = {
    1: [("French fries", 60), ("Paneer Tikka", 80), ("Spring rolls", 50),
        ("Chicken wings", 100), ("Cheese balls", 70)],
    2: [("Paneer butter masala", 150), ("Chicken curry", 200), ("Mutton curry", 250),
        ("Dal makhani", 100), ("Chole bhature", 120)],
    3: [("Cold drink", 40), ("Lassi", 30), ("Tea", 10),
        ("Coffee", 20), ("Lemonade", 30)],
    4: [("Gulab jamun", 40), ("Rasgulla", 30), ("Rasmalai", 50),
        ("Kulfi", 20), ("Ice cream", 30)],
    5: [("Ice cream", 70), ("Brownie", 90)],
    6: [("Spring Roll", 100), ("Chilli Paneer", 140)],
    7: [("Tomato Soup", 80), ("Sweet Corn Soup", 85)],
    8: [("Kesar pista", 70), ("Choco chips", 80)]
}

# Category names for display
CATEGORIES = {
    1: "Starters",
    2: "Main Course",
    3: "Drinks",
    4: "Desserts",
    5: "Ice Cream",
    6: "Chinese",
    7: "Soups",
    8: "Food Combos"
}

def display_categories():
    """Returns a formatted string of category numbers and names."""
    return "\n".join(f"{key}. {value}" for key, value in CATEGORIES.items())

def display_main_menu():
    """Returns only the category list for display in the GUI."""
    return display_categories()

def display_menu(category):
    """Returns the list of items for a given category."""
    return MENU.get(category, [])

def take_order(category, item_number, quantity):
    """Returns item details and total quantity."""
    try:
        item_name, price = MENU[category][item_number - 1]
        return item_name, price, quantity
    except (IndexError, KeyError):
        raise ValueError("Invalid category or item number")