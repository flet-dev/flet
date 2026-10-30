import 'package:flutter/widgets.dart';
import 'package:lucide_icons_flutter/lucide_icons.dart';

List<IconData> lucideIcons = [
  {% for name, code in icons -%}
  LucideIcons.{{ name }},
  {% endfor -%}
];
