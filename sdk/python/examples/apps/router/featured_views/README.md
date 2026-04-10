# Full App with Managed Views and NavigationRail

Demonstrates a complete app structure with `manage_views=True`, NavigationRail, and multiple layout patterns.

## Structure

- **RootLayout** — pathless `outlet=True` layout with NavigationRail. Returns a View with fixed `route="/"` to avoid transition animation between top-level pages.
- **Home** — simple content, rendered in RootLayout's outlet.
- **Projects** — stacked views. List → Details pushes a new view (back button works). Components return regular controls; RootLayout provides the View.
- **Settings** — tabbed layout using `outlet=True`. General/Account are sibling routes under SettingsLayout. Switching tabs swaps outlet content within the same view (no transition).

## View Stack

- `/` → 1 view: RootLayout(Home)
- `/projects` → 1 view: RootLayout(ProjectsList) — nav rail switches, no animation
- `/projects/1` → 2 views: RootLayout(ProjectsList), RootLayout(ProjectDetails) — slide transition, back button
- `/settings/general` → 1 view: RootLayout(SettingsLayout(General)) — nav rail switches
- `/settings/account` → 1 view: RootLayout(SettingsLayout(Account)) — tab swap, no animation
