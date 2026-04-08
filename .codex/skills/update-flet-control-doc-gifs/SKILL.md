---
name: update-flet-control-doc-gifs
description: Create or update Flet control screenshots and GIFs that are generated from integration tests and shown in docs. Use when working on `sdk/python/packages/flet/integration_tests/examples`, refreshing static or interactive golden screenshots, replacing old example media images or GIFs with generated test assets, or copying rendered screenshot and GIF assets into `website/static/docs/test-images`.
---

# Update Flet Control Doc Gifs

Use this skill after the integration test structure is already in place and the task is to capture doc-ready screenshots or interactive GIF states from integration tests.

## Workflow

1. Locate the example-backed integration test under `sdk/python/packages/flet/integration_tests/examples`.
2. Prefer extending an existing `test_basic` or similar interaction test instead of creating a second flow test.
3. Build the visual sequence with deterministic states:
- set `page.enable_screenshots = True`
- set `theme_mode` when visuals matter
- set fixed page size before screenshots
- call `pump_and_settle()` after each interaction
4. Capture only states that are visually meaningful:
- before interaction
- hover state
- popup/menu/dialog open
- reopened state that proves persistence
- single static screenshots when one frame is enough for docs
- do not keep screenshots taken after a click if the UI closes and the state is not visible
5. Use `assert_screenshot(...)` for regular golden screenshots and `create_gif([...], "<flow_name>", duration=...)` only when the docs benefit from an animated flow.
6. Update docs to use the generated screenshot or GIF, not an old media asset from `examples/.../media`, when the integration-test asset is now the better docs artifact.
7. Ensure the generated screenshot or GIF is available under `website/static/docs/test-images/...` so the docs page can render it.

## Naming

- Use short screenshot names that describe visible states, for example `before_click`, `hover_popup`, `popup_open`, `checked_item_reopened`.
- Use one flow GIF name per control/example, for example `app_bar_flow`.
- Use descriptive static screenshot names when the asset is docs-facing, for example `image_for_docs`, `popup_open`, or `checked_item_reopened`.
- Keep screenshot names stable because they become golden filenames.

## Docs Update Rules

- Control docs usually point to generated assets through `frontMatter.example_images`.
- If a docs page still uses `frontMatter.example_media + '/old.png'` or `frontMatter.example_media + '/old.gif'`, replace it with `frontMatter.example_images + '/<asset>'` when the generated integration-test asset is the new source of truth.
- Generated screenshots and GIFs from integration tests are commonly stored at `sdk/python/packages/flet/integration_tests/examples/.../golden/macos/<control>/`.
- Copy the final screenshot or GIF to `website/static/docs/test-images/examples/<bucket>/golden/macos/<control>/` when it is not already present there.

## Verification Checklist

- The interaction test still reflects the example behavior.
- Every screenshot included in a GIF is visibly different and useful.
- The GIF duration is intentional; prefer shorter loops for hover/click flows unless the interaction needs more time.
- The docs page references the new screenshot or GIF path.
- The referenced screenshot or GIF actually exists under `website/static/docs/test-images/...`.
- Remove or stop referencing obsolete media screenshots or GIFs only when the new generated asset fully replaces them.

## References

- `sdk/python/packages/flet/integration_tests/examples`
- `sdk/python/packages/flet/integration_tests/examples/controls/material/test_alert_dialog.py`
- `sdk/python/packages/flet/integration_tests/examples/controls/material/test_app_bar.py`
- `website/docs/controls`
- `website/static/docs/test-images`
