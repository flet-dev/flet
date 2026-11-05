import 'package:material_ui/material_ui.dart';

List<IconData> materialIcons = [
  {% for name, code in icons -%}
  Icons.{{ name }},
  {% endfor -%}
];
