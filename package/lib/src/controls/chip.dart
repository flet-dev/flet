import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';
import 'package:flet/src/flet_app_services.dart';

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

    final server = FletAppServices.of(context).server;
    bool onClick = widget.control.attrBool("onclick", false)!;

    Function()? onClickHandler = onClick && !disabled
        ? () {
            debugPrint("Chip ${widget.control.id} clicked!");
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "click",
                eventData: "");
          }
        : null;

    return constrainedControl(
        context,
        // Chip(
        //   //label: Text(control.attrString("label", "")!),
        //   //label: createControl(widget.control, contentCtrls.first.id, disabled)
        //   label: createControl(widget.control, labelCtrls.first.id, disabled),
        //   backgroundColor: bgcolor,
        // ),
        InputChip(
          label: createControl(widget.control, labelCtrls.first.id, disabled),
          backgroundColor: bgcolor,
          onPressed: onClickHandler,
        ),
        widget.parent,
        widget.control);
  }
}
