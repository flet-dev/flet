import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class VerticalDividerControl extends StatelessWidget {
  final Control control;

  const VerticalDividerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("VerticalDivider build: ${control.id}");

    var divider = VerticalDivider(
      width: control.getDouble("width"),
      thickness: control.getDouble("thickness"),
      color: control.getColor("color", context),
      indent: control.getDouble("leading_indent"),
      endIndent: control.getDouble("trailing_indent"),
      radius: control.getBorderRadius("radius"),
    );

    return BaseControl(control: control, child: divider);
  }
}
