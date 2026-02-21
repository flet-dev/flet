import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class RotatedBoxControl extends StatelessWidget {
  final Control control;

  const RotatedBoxControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("RotatedBox build: ${control.id}");

    return LayoutControl(
      control: control,
      child: RotatedBox(
        quarterTurns: control.getInt("quarter_turns", 0)!,
        child: control.buildWidget("content"),
      ),
    );
  }
}
