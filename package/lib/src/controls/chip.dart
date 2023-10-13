import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';

class ChipControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const ChipControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<ChipControl> createState() => _ChipControlState();
}

class _ChipControlState extends State<ChipControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("Chip build: ${widget.control.id}");

    // var contentCtrls =
    //     children.where((c) => c.name == "content" && c.isVisible);
    var labelCtrls =
        widget.children.where((c) => c.name == "label" && c.isVisible);
    if (labelCtrls.isEmpty) {
      return const ErrorControl("Chip must have label specified.");
    }
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var bgcolor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("bgcolor", "")!);

    return constrainedControl(
        context,
        Chip(
          //label: Text(control.attrString("label", "")!),
          //label: createControl(widget.control, contentCtrls.first.id, disabled)
          label: createControl(widget.control, labelCtrls.first.id, disabled),
          backgroundColor: bgcolor,
        ),

        //elevation: control.attrDouble("elevation"),
        //margin: parseEdgeInsets(control, "margin"),
        //color: HexColor.fromString(
        //     Theme.of(context), control.attrString("color", "")!),
        // shadowColor: HexColor.fromString(
        //     Theme.of(context), control.attrString("shadowColor", "")!),
        // surfaceTintColor: HexColor.fromString(
        //     Theme.of(context), control.attrString("surfaceTintColor", "")!),
        // child: contentCtrls.isNotEmpty
        //     ? createControl(control, contentCtrls.first.id, disabled)
        //     : null),
        widget.parent,
        widget.control);
  }
}
