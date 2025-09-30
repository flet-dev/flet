import 'package:flutter/material.dart';

List<IconData> materialIcons = [
  {% for name, code in icons -%}
  Icons.{{ name }},
  {% endfor -%}
];
