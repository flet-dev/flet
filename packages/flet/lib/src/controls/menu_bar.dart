import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import '../widgets/error.dart';
import 'base_controls.dart';

class MenuBarControl extends StatefulWidget {
  final Control control;

  const MenuBarControl({super.key, required this.control});

  @override
  State<MenuBarControl> createState() => _MenuBarControlState();
}

class _MenuBarControlState extends State<MenuBarControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("MenuBar build: ${widget.control.id}");

    var controls = widget.control.buildWidgets("controls");
    if (controls.isEmpty) {
      return const ErrorControl(
          "MenuBar must have at minimum one visible child control");
    }
    final menuBar = MenuBar(
        style: widget.control.getMenuStyle("style", Theme.of(context)),
        clipBehavior:
            widget.control.getClipBehavior("clip_behavior", Clip.none)!,
        children: controls);

    return ConstrainedControl(control: widget.control, child: menuBar);
  }
}
