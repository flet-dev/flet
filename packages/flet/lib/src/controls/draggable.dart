import 'dart:convert';

import 'package:flet/src/extensions/control.dart';
import 'package:flet/src/utils/misc.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../widgets/error.dart';

class DraggableControl extends StatelessWidget {
  final Control control;

  const DraggableControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("DragTarget build: ${control.id}");
    var group = control.getString("group", "default")!;
    var content = control.buildWidget("content");

    if (content == null) {
      return const ErrorControl("Draggable.content must be visible");
    }

    var data = json.encode({"id": control.id, "group": group});

    return Draggable<String>(
      data: data,
      axis: control.getAxis("axis"),
      affinity: control.getAxis("affinity"),
      maxSimultaneousDrags: control.getInt("max_simultaneous_drags"),
      onDragStarted: () => control.triggerEvent("drag_start"),
      onDragCompleted: () => control.triggerEvent("drag_complete", group),
      childWhenDragging: control.buildWidget("content_when_dragging"),
      feedback: MouseRegion(
        cursor: SystemMouseCursors.grabbing,
        child: control.buildWidget("content_feedback") ??
            Opacity(opacity: 0.5, child: content),
      ),
      child: MouseRegion(
        cursor: SystemMouseCursors.grab,
        child: content,
      ),
    );
  }
}
