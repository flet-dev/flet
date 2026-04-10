# Nested Routes with Shared Layout

Demonstrates `manage_views=True` combined with `outlet=True` for shared layouts.

ProductsLayout wraps both ProductsList and ProductDetails via outlet. Each child is its own View with the shared layout (AppBar + footer), so AppBar back works: Details → List → Home.

- `outlet=True` on ProductsLayout makes it a layout that wraps each child view
- Leaf components return regular controls (not Views) — the layout provides the View
- `/` → 1 view (Home)
- `/products` → 2 views (Home, ProductsLayout wrapping ProductsList)
- `/products/1` → 3 views (Home, ProductsLayout wrapping ProductsList, ProductsLayout wrapping ProductDetails)
