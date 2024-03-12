import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class DraggableControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const DraggableControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

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
        ? createControl(control, contentCtrls.first.id, disabled,
            parentAdaptive: parentAdaptive)
        : null;

    Widget? childWhenDragging = contentWhenDraggingCtrls.isNotEmpty
        ? createControl(control, contentWhenDraggingCtrls.first.id, disabled,
            parentAdaptive: parentAdaptive)
        : null;

    Widget? childFeedback = contentFeedbackCtrls.isNotEmpty
        ? createControl(control, contentFeedbackCtrls.first.id, disabled,
            parentAdaptive: parentAdaptive)
        : null;

    if (child == null) {
      return const ErrorControl("Draggable should have content.");
    }

    var data = json.encode({"id": control.id, "group": group});

    return Draggable<String>(
      data: data,
      childWhenDragging: childWhenDragging,
      feedback: MouseRegion(
        cursor: SystemMouseCursors.grabbing,
        child: childFeedback ?? Opacity(opacity: 0.5, child: child),
      ),
      onDragStarted: () {
        debugPrint("Draggable.onDragStarted ${control.id}");
        backend.triggerControlEvent(control.id, "dragStart");
      },
      onDragCompleted: () {
        debugPrint("Draggable.onDragCompleted ${control.id}");
        backend.triggerControlEvent(control.id, "dragComplete");
      },
      child: MouseRegion(
        cursor: SystemMouseCursors.grab,
        child: child,
      ),
    );
  }
}
