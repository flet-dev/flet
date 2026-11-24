---
name: update-flet-control-doc-gifs
description: Create or update Flet control screenshots and GIFs that are generated from integration tests and shown in docs. Use when working on `sdk/python/packages/flet/integration_tests/examples`, refreshing static or interactive golden screenshots, or replacing old example media images or GIFs with generated test assets.
---

# Update Flet Control Doc Gifs

Use this skill after the integration test structure is already in place and the task is to capture doc-ready screenshots or interactive GIF states from integration tests.

## Workflow

1. Locate the example-backed integration test under `sdk/python/packages/flet/integration_tests/examples`.
2. Prefer extending an existing interaction test instead of creating a second flow test.
3. Build the visual sequence with deterministic states:
- set `page.enable_screenshots = True`
- set `theme_mode` when visuals matter
- set fixed page size before screenshots
- prefer finding controls by visible text or other stable user-facing content; add a `key` only when there is no reliable human-facing locator
- call `pump_and_settle()` after each interaction
4. Capture only states that are visually meaningful:
- before interaction
- hover state
- popup/menu/dialog open
- reopened state that proves persistence
- single static screenshots when one frame is enough for docs
- do not keep screenshots taken after a click if the UI closes and the state is not visible
5. Use `assert_screenshot(...)` for regular golden screenshots and `create_gif([...], "<flow_name>", duration=...)` only when the docs benefit from an animated flow.
 - Prefer storing only asserted or docs-facing states as named screenshots; keep intermediate hover/click frames in memory and pass them directly to `create_gif(...)` when they do not need standalone golden files.
6. Update docs to use the generated screenshot or GIF, not an old media asset from `examples/.../media`, when the integration-test asset is now the better docs artifact.
7. Update docs references to point at the intended generated screenshot or GIF path, but do not copy generated assets into `website/static/docs/test-images/...` as part of this workflow.

## Naming

- Use short screenshot names that describe visible states, for example `before_click`, `hover_popup`, `popup_open`, `checked_item_reopened`.
- Use one flow GIF name per control/example, for example `app_bar_flow`.
- Use descriptive static screenshot names when the asset is docs-facing, for example `image_for_docs`, `popup_open`, or `checked_item_reopened`.
- Give the integration test a behavior-based name such as `test_actions_and_popup_menu`; avoid placeholder names like `test_basic` when the test covers a specific flow.
- Keep screenshot names stable because they become golden filenames.

## Docs Update Rules

- Control docs usually point to generated assets through `frontMatter.example_images`.
- If a docs page still has `example_images` pointing at example media instead of generated test images, update that front matter first so the page has a single source of truth for screenshots and GIFs.
- When a docs page has multiple example sections, add the generated screenshot or GIF directly under the matching `CodeExample` block so each visual stays paired with the example it demonstrates.
- If a docs page still uses `frontMatter.example_media + '/old.png'` or `frontMatter.example_media + '/old.gif'`, replace it with `frontMatter.example_images + '/<asset>'` when the generated integration-test asset is the new source of truth.
- Generated screenshots and GIFs from integration tests are commonly stored at `sdk/python/packages/flet/integration_tests/examples/.../golden/macos/<control>/`.
- Do not copy generated screenshots or GIFs into `website/static/docs/test-images/...` as part of this skill. Keep the work limited to tests and docs references unless the user explicitly asks for a copy.

## Verification Checklist

- The interaction test still reflects the example behavior.
- Every screenshot included in a GIF is visibly different and useful.
- The GIF duration is intentional; prefer shorter loops for hover/click flows unless the interaction needs more time.
- The docs front matter points to the generated test-images location rather than stale example media paths.
- The docs page references the new screenshot or GIF path.
- The generated screenshot or GIF exists in the integration-test golden directory at the path implied by the test names.
- Remove or stop referencing obsolete media screenshots or GIFs only when the new generated asset fully replaces them.

## References

- `sdk/python/packages/flet/integration_tests/examples`
- `sdk/python/packages/flet/integration_tests/examples/controls/material/test_alert_dialog.py`
- `sdk/python/packages/flet/integration_tests/examples/controls/material/test_app_bar.py`
- `website/docs/controls`
