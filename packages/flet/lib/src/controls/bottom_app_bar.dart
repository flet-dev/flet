import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class BottomAppBarControl extends StatelessWidget {
  final Control control;

  const BottomAppBarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("BottomAppBarControl build: ${control.id}");

    var bottomAppBar = BottomAppBar(
      clipBehavior: control.getClipBehavior("clip_behavior", Clip.none)!,
      padding: control.getPadding("padding"),
      height: control.getDouble("height"),
      elevation: control.getDouble("elevation"),
      shape: control.getNotchedShape("shape", Theme.of(context)),
      shadowColor: control.getColor("shadow_color", context),
      surfaceTintColor: control.getColor("surface_tint_color", context),
      color: control.getColor("bgcolor", context),
      notchMargin: control.getDouble("notch_margin", 4.0)!,
      child: control.buildWidget("content"),
    );

    return ConstrainedControl(control: control, child: bottomAppBar);
  }
}
