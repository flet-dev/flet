import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_control_state.dart';

class BottomAppBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const BottomAppBarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  State<BottomAppBarControl> createState() => _BottomAppBarControlState();
}

class _BottomAppBarControlState extends State<BottomAppBarControl>
    with FletControlState {
  @override
  Widget build(BuildContext context) {
    debugPrint("BottomAppBarControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);

    var s = widget.control.attrString("shape");
    NotchedShape? shape;
    if (s == "circular") {
      shape = const CircularNotchedRectangle();
    } else if (s == "auto") {
      shape = const AutomaticNotchedShape(ContinuousRectangleBorder());
    }

    var elevation = widget.control.attrDouble("elevation", 0);
    if (elevation! < 0) {
      return const ErrorControl(
          "The Elevation of the BottomAppBar must be greater than or equal to 0 !");
    }

    var clipBehavior = Clip.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            widget.control.attrString("clipBehavior", "")!.toLowerCase(),
        orElse: () => Clip.none);
    var bottomAppBar = withControls(
        widget.children
            .where((c) => c.isVisible && c.name == null)
            .map((c) => c.id), (content, viewModel) {
      return BottomAppBar(
        clipBehavior: clipBehavior,
        padding: parseEdgeInsets(widget.control, "padding"),
        height: widget.control.attrDouble("height"),
        elevation: elevation,
        shape: shape,
        shadowColor: HexColor.fromString(
            Theme.of(context), widget.control.attrString("shadowColor", "")!),
        surfaceTintColor: HexColor.fromString(Theme.of(context),
            widget.control.attrString("surfaceTintColor", "")!),
        color: HexColor.fromString(
            Theme.of(context), widget.control.attrString("bgColor", "")!),
        notchMargin: widget.control.attrDouble("notchMargin", 4.0)!,
        child: contentCtrls.isNotEmpty
            ? createControl(widget.control, contentCtrls.first.id, disabled)
            : null,
      );
    });

    return constrainedControl(
        context, bottomAppBar, widget.parent, widget.control);
  }
}
