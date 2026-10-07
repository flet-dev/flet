# flutter_colorpicker (vendored)

A copy of [flutter_colorpicker](https://github.com/mchome/flutter_colorpicker)
1.1.0 (`lib/`), MIT licensed (see `LICENSE`).

It's vendored because its pickers are built on the Flutter SDK's Material
widgets, which fail with "No Material widget found" inside the `material_ui`
app Flet renders with, and no release built on `material_ui` exists.

Changes from 1.1.0: imports `package:material_ui/material_ui.dart` instead of
`package:flutter/material.dart` (`dart fix --code=migrate_design_widgets`).
Replace it with the published package once it moves to `material_ui`.
