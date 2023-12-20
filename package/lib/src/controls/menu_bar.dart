import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/menu.dart';
import 'create_control.dart';
import 'error.dart';

class MenuBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const MenuBarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  State<MenuBarControl> createState() => _MenuBarControlState();
}

class _MenuBarControlState extends State<MenuBarControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("MenuBar build: ${widget.control.id}");

    var ctrls = widget.children.where((c) => c.isVisible).toList();
    if (ctrls.isEmpty) {
      return const ErrorControl(
        "MenuBar must have at least one child control",
      );
    }
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var clipBehavior = Clip.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            widget.control.attrString("clipBehavior", "")!.toLowerCase(),
        orElse: () => Clip.none);

    var theme = Theme.of(context);

    var style = parseMenuStyle(Theme.of(context), widget.control, "style");

    MenuBar? menuBar = MenuBar(
      style: style,
      clipBehavior: clipBehavior,
      children: ctrls.map((c) => createControl(widget.control, c.id, disabled)).toList(),
    );

    return constrainedControl(context, menuBar, widget.parent, widget.control);
  }
}
