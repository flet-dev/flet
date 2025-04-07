import 'package:flet/src/utils/colors.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import 'base_controls.dart';

class PlaceholderControl extends StatelessWidget {
  final Control control;

  const PlaceholderControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Placeholder build: ${control.id}");

    final placeholder = Placeholder(
        fallbackHeight: control.getDouble("fallback_height", 400.0)!,
        fallbackWidth: control.getDouble("fallback_width", 400.0)!,
        color: control.getColor("color", context, const Color(0xFF455A64))!,
        strokeWidth: control.getDouble("stroke_width", 2.0)!,
        child: control.buildWidget("content"));

    return ConstrainedControl(control: control, child: placeholder);
  }
}
