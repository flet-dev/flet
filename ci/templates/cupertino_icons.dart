import 'package:flutter/cupertino.dart';

List<IconData> cupertinoIcons = [
  {% for name, code in icons -%}
  CupertinoIcons.{{ name }},
  {% endfor -%}
];
