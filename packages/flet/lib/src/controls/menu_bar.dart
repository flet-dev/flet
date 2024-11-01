import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/menu.dart';
import '../utils/others.dart';
import 'create_control.dart';
import 'error.dart';

class MenuBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const MenuBarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

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
          "MenuBar must have at minimum one visible child control");
    }

    return constrainedControl(
        context,
        MenuBar(
          style: parseMenuStyle(Theme.of(context), widget.control, "style"),
          clipBehavior:
              parseClip(widget.control.attrString("clipBehavior"), Clip.none)!,
          children: ctrls
              .map((c) => createControl(widget.control, c.id,
                  widget.control.isDisabled || widget.parentDisabled,
                  parentAdaptive:
                      widget.control.isAdaptive ?? widget.parentAdaptive))
              .toList(),
        ),
        widget.parent,
        widget.control);
  }
}
