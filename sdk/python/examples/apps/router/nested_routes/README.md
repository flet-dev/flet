# Nested Routes with View Stack

Demonstrates `manage_views=True` with nested route hierarchy. Each route component returns a `View` with its own AppBar.

- Swipe-back and AppBar back button work automatically
- Home is a pathless root, so it's always in the view stack
- `/` → 1 view (Home)
- `/products` → 2 views (Home, Products) — back to Home
- `/products/1` → 3 views (Home, Products, Product Details) — back to Products
