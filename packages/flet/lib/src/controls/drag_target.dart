import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class DragTargetEvent {
  final String srcId;
  final double x;
  final double y;

  DragTargetEvent({
    required this.srcId,
    required this.x,
    required this.y,
  });

  Map<String, dynamic> toJson() => <String, dynamic>{
        'src_id': srcId,
        'x': x,
        'y': y,
      };
}

class DragTargetControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const DragTargetControl(
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
    bool disabled = control.isDisabled || parentDisabled;

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled,
            parentAdaptive: parentAdaptive)
        : null;

    if (child == null) {
      return const ErrorControl("DragTarget should have content.");
    }

    return DragTarget<String>(
      builder: (
        BuildContext context,
        List<dynamic> accepted,
        List<dynamic> rejected,
      ) {
        debugPrint(
            "DragTarget.builder ${control.id}: accepted=${accepted.length}, rejected=${rejected.length}");
        return child;
      },
      onMove: (details) {
        var data = details.data;
        debugPrint("DragTarget.onMove ${control.id}: $data");
        var jd = json.decode(data);
        var srcId = jd["id"] as String;
        backend.triggerControlEvent(
            control.id,
            "move",
            json.encode(DragTargetEvent(
                    srcId: srcId, x: details.offset.dx, y: details.offset.dy)
                .toJson()));
      },
      onWillAcceptWithDetails: (details) {
        var data = details.data;
        debugPrint("DragTarget.onWillAcceptWithDetails ${control.id}: $data");
        String srcGroup = "";
        var jd = json.decode(data);
        srcGroup = jd["group"] as String;
        var groupsEqual = srcGroup == group;
        backend.triggerControlEvent(
            control.id, "will_accept", groupsEqual.toString());
        return groupsEqual;
      },
      onAcceptWithDetails: (details) {
        var data = details.data;
        debugPrint("DragTarget.onAcceptWithDetails ${control.id}: $data");
        var jd = json.decode(data);
        var srcId = jd["id"] as String;
        backend.triggerControlEvent(
            control.id,
            "accept",
            json.encode(DragTargetEvent(
                    srcId: srcId, x: details.offset.dx, y: details.offset.dy)
                .toJson()));
      },
      onLeave: (data) {
        debugPrint("DragTarget.onLeave ${control.id}: $data");
        String srcId = "";
        if (data != null) {
          var jd = json.decode(data);
          srcId = jd["id"] as String;
        }
        backend.triggerControlEvent(control.id, "leave", srcId);
      },
    );
  }
}
