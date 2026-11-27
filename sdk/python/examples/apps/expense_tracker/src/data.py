"""Available currencies and category style choices."""

CURRENCIES = {
    "USD": ("US dollar", "$"),
    "EUR": ("Euro", "€"),
    "GBP": ("British pound", "£"),
    "CAD": ("Canadian dollar", "CA$"),
    "AUD": ("Australian dollar", "A$"),
    "INR": ("Indian rupee", "₹"),
    "CHF": ("Swiss franc", "CHF "),
}
COLOR_NAMES = {
    "teal": "Teal",
    "indigo": "Indigo",
    "amber": "Amber",
    "pink": "Pink",
    "slate": "Slate",
    "blue": "Blue",
    "purple": "Purple",
    "orange": "Orange",
}
ICON_NAMES = {
    "food": "Food",
    "transport": "Transport",
    "bills": "Bills",
    "fun": "Fun",
    "other": "Other",
    "shopping": "Shopping",
    "home": "Home",
    "gift": "Gifts",
}
DEFAULT_CATEGORY_STYLES = (
    ("Food", "teal", "food"),
    ("Transport", "indigo", "transport"),
    ("Bills", "amber", "bills"),
    ("Fun", "pink", "fun"),
    ("Other", "slate", "other"),
)
