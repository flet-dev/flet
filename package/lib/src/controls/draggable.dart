import 'dart:convert';

import 'error.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';

class DraggableControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const DraggableControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("DragTarget build: ${control.id}");

    var group = control.attrString("group", "");
    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    var contentWhenDraggingCtrls =
        children.where((c) => c.name == "content_when_dragging" && c.isVisible);
    var contentFeedbackCtrls =
        children.where((c) => c.name == "content_feedback" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled)
        : null;

    Widget? childWhenDragging = contentWhenDraggingCtrls.isNotEmpty
        ? createControl(control, contentWhenDraggingCtrls.first.id, disabled)
        : null;

    Widget? childFeedback = contentFeedbackCtrls.isNotEmpty
        ? createControl(control, contentFeedbackCtrls.first.id, disabled)
        : null;

    if (child == null) {
      return const ErrorControl("Draggable should have content.");
    }

    var data = json.encode({"id": control.id, "group": group});

    return Draggable<String>(
      data: data,
      child: MouseRegion(
        cursor: SystemMouseCursors.grab,
        child: child,
      ),
      childWhenDragging: childWhenDragging,
      feedback: MouseRegion(
        cursor: SystemMouseCursors.grabbing,
        child: childFeedback ?? Opacity(opacity: 0.5, child: child),
      ),
      // dragAnchorStrategy: (d, context, offset) {
      //   debugPrint("dragAnchorStrategy: ${offset.dx}, ${offset.dy}");
      //   return offset;
      // }
      //feedbackOffset: const Offset(-30, -30),
    );
  }
}
