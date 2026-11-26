// GENERATED FILE, DO NOT EDIT. To update it, run from the root of the repository:
//
//   uv run .github/scripts/generate_icons.py
//
// Fluent UI System Icons (MIT), drawn from fonts/FluentSystemIcons-Resizable.ttf.
// The Nth entry is the icon whose packed value is `(4 << 16) | N`.

import 'package:flutter/widgets.dart' show IconData;

const List<IconData> fluentIcons = [
  {% for name, code in icons -%}
  IconData(0x{{ '%04x' % code }}, fontFamily: 'FluentIcons', fontPackage: 'flet_fluent_ui'), // {{ name }}
  {% endfor -%}
];
