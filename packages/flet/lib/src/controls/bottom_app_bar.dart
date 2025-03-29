import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

class BottomAppBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const BottomAppBarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  State<BottomAppBarControl> createState() => _BottomAppBarControlState();
}

class _BottomAppBarControlState extends State<BottomAppBarControl>
    with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint("BottomAppBarControl build: ${widget.control.id}");

    bool disabled = widget.control.disabled || widget.parentDisabled;
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.visible);

    var shape = parseNotchedShape(widget.control.getString("shape"));

    var elevation = widget.control.getDouble("elevation", 0)!;

    var clipBehavior =
        parseClip(widget.control.getString("clipBehavior"), Clip.none)!;
    var bottomAppBar = withControls(
        widget.children
            .where((c) => c.visible && c.name == null)
            .map((c) => c.id), (content, viewModel) {
      return BottomAppBar(
        clipBehavior: clipBehavior,
        padding: parseEdgeInsets(widget.control, "padding"),
        height: widget.control.getDouble("height"),
        elevation: elevation,
        shape: shape,
        shadowColor: widget.control.getColor("shadowColor", context),
        surfaceTintColor: widget.control.getColor("surfaceTintColor", context),
        color: widget.control.getColor("bgColor", context),
        notchMargin: widget.control.getDouble("notchMargin", 4.0)!,
        child: contentCtrls.isNotEmpty
            ? createControl(widget.control, contentCtrls.first.id, disabled,
                parentAdaptive: widget.parentAdaptive)
            : null,
      );
    });

    return constrainedControl(
        context, bottomAppBar, widget.parent, widget.control);
  }
}
