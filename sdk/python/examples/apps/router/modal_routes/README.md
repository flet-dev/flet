# Modal routes

Routes marked `modal=True` are rendered as fullscreen-dialog overlays on
top of the previous location's view stack. Closing the modal pops it
without rebuilding the views underneath.

This example demonstrates both modes:

- **`/settings`** — a *global* modal declared at the top level. Reachable
  from `/`, `/items`, `/items/<id>` — closing returns to whichever URL was
  active when it opened. Deep-linking to `/settings` directly defaults the
  base to `/`.

- **`/items/<id>/edit`** — a *local* modal declared as a child of
  `/items/:id`. The URL embeds the item id, so deep-linking restores the
  full stack `[ItemList, ItemDetails(id), EditItemModal]` from URL alone.

## Run

```bash
flet run
```

## What to try

1. From `Home`, tap "Open Settings" → modal slides up over Home. Close →
   back to Home with no rebuild.
2. Navigate `Home → Items → Apples` → tap "Edit" → local modal slides over
   the Apples detail view. Close → back to Apples with the detail view
   still mounted.
3. From Apples detail, tap "Open Settings" → modal slides up over the
   detail. Close → back to Apples detail (not Home).
4. Paste `/items/2/edit` into the URL — the stack rebuilds and the modal
   opens directly. Close → `/items/2`.
