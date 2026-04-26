# App Settings Drawer

Demonstrates a NavigationDrawer with deep-linkable tabs, driven by nested routes.

## Routes

- `/` — Home
- `/apps` — Apps list
- `/apps/:app_id` — App details (drawer closed)
- `/apps/:app_id/settings/general` — App details with drawer open on General tab
- `/apps/:app_id/settings/permissions` — App details with drawer open on Permissions tab

## How it works

The `:app_id` route has `outlet=True` and two child routes for the settings tabs.
`AppDetails` always renders as a single View. Inside it:

- `use_route_outlet()` returns the matched tab component (or `None` if just `/apps/:app_id`)
- A `use_effect` watches whether the outlet is set and calls `page.open(drawer)` /
  `page.close(drawer)` accordingly
- The drawer's `on_dismiss` navigates back to `/apps/:app_id` when the user swipes
  the drawer away
- Tab buttons inside the drawer use `is_route_active(..., exact=True)` to highlight
  the current tab and navigate between tabs
- The View's `route` is the same (`/apps/:app_id`) regardless of the active tab,
  so Flutter's Navigator doesn't animate the View when switching tabs

## View stack

- `/` — 1 view (Home)
- `/apps` — 2 views (Home, AppsList)
- `/apps/2` — 3 views (Home, AppsList, AppDetails); back button to AppsList
- `/apps/2/settings/general` — same 3 views; drawer slides open on top
- `/apps/2/settings/permissions` — same 3 views; drawer stays open, tab content swaps
