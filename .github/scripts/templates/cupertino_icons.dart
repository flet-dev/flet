import 'package:cupertino_ui/cupertino_ui.dart';

List<IconData> cupertinoIcons = [
  {% for name, code in icons -%}
  CupertinoIcons.{{ name }},
  {% endfor -%}
];
