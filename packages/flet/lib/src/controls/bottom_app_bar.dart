import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class BottomAppBarControl extends StatelessWidget {
  final Control control;

  const BottomAppBarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("BottomAppBarControl build: ${control.id}");

    final theme = Theme.of(context);
    var borderRadius = control.getBorderRadius("border_radius");
    final clipBehavior = control.getClipBehavior(
        "clip_behavior",
        borderRadius != null && borderRadius != BorderRadius.zero
            ? Clip.antiAlias
            : Clip.none)!;

    Widget bottomAppBar = BottomAppBar(
      clipBehavior: clipBehavior,
      padding: control.getPadding("padding"),
      height: control.getDouble("height"),
      elevation: control.getDouble("elevation"),
      shape: control.getNotchedShape("shape", theme),
      shadowColor: control.getColor("shadow_color", context),
      color: control.getColor("bgcolor", context),
      notchMargin: control.getDouble("notch_margin", 4.0)!,
      child: control.buildWidget("content"),
    );

    if (borderRadius != null && borderRadius != BorderRadius.zero) {
      bottomAppBar = ClipRRect(
        borderRadius: borderRadius,
        // can't use Clip.none here, so fallback to Clip.antiAlias in that case
        clipBehavior: clipBehavior == Clip.none ? Clip.antiAlias : clipBehavior,
        child: bottomAppBar,
      );
    }

    return LayoutControl(control: control, child: bottomAppBar);
  }
}
