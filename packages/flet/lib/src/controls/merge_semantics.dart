import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import 'base_controls.dart';

class MergeSemanticsControl extends StatelessWidget {
  final Control control;

  const MergeSemanticsControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("MergeSemantics build: ${control.id}");

    return LayoutControl(
        control: control,
        child: MergeSemantics(child: control.buildWidget("content")));
  }
}
