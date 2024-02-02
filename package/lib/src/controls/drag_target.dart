import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_control_stateless_mixin.dart';

class DragTargetAcceptEvent {
  final String srcId;
  final double x;
  final double y;

  DragTargetAcceptEvent({
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

class DragTargetControl extends StatelessWidget with FletControlStatelessMixin {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const DragTargetControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

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
      onWillAccept: (data) {
        debugPrint("DragTarget.onAccept ${control.id}: $data");
        String srcGroup = "";
        if (data != null) {
          var jd = json.decode(data);
          srcGroup = jd["group"] as String;
        }
        var groupsEqual = srcGroup == group;
        sendControlEvent(
            context, control.id, "will_accept", groupsEqual.toString());
        return groupsEqual;
      },
      onAcceptWithDetails: (details) {
        var data = details.data;
        debugPrint("DragTarget.onAcceptWithDetails ${control.id}: $data");
        var jd = json.decode(data);
        var srcId = jd["id"] as String;
        sendControlEvent(
            context,
            control.id,
            "accept",
            json.encode(DragTargetAcceptEvent(
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
        sendControlEvent(context, control.id, "leave", srcId);
      },
    );
  }
}
