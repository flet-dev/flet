import 'package:fluent_ui/fluent_ui.dart' show FluentIcons, IconData;

List<IconData> fluentIcons = [
  {% for name, code in icons -%}
  FluentIcons.{{ name }},
  {% endfor -%}
];
