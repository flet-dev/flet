import 'dart:convert';

import 'package:flet/src/extensions/control.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../widgets/error.dart';

class DragTargetEvent {
  final String srcId;
  final double x;
  final double y;

  DragTargetEvent({
    required this.srcId,
    required this.x,
    required this.y,
  });

  Map<String, dynamic> toMap() =>
      <String, dynamic>{'src_id': srcId, 'x': x, 'y': y};
}

class DragTargetControl extends StatelessWidget {
  final Control control;

  const DragTargetControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("DragTarget build: ${control.id}");

    var group = control.getString("group", "default")!;
    var content = control.buildWidget("content");

    if (content == null) {
      return const ErrorControl("DragTarget.content must be visible");
    }

    return DragTarget<String>(
      builder: (
        BuildContext context,
        List<dynamic> accepted,
        List<dynamic> rejected,
      ) {
        return content;
      },
      onMove: (DragTargetDetails<String> details) {
        var data = json.decode(details.data);
        control.triggerEvent(
            "move",
            DragTargetEvent(
                    srcId: data["id"],
                    x: details.offset.dx,
                    y: details.offset.dy)
                .toMap());
      },
      onWillAcceptWithDetails: (DragTargetDetails<String> details) {
        var data = json.decode(details.data);
        var srcGroup = data["group"] as String;
        var groupMatch = srcGroup == group;
        control.triggerEvent("will_accept", groupMatch);
        return groupMatch;
      },
      onAcceptWithDetails: (DragTargetDetails<String> details) {
        var data = json.decode(details.data);
        control.triggerEvent(
            "accept",
            DragTargetEvent(
                    srcId: data["id"],
                    x: details.offset.dx,
                    y: details.offset.dy)
                .toMap());
      },
      onLeave: (String? data) {
        int? srcId;
        if (data != null) {
          var jd = json.decode(data);
          srcId = jd["id"];
        }
        control.triggerEvent("leave", srcId);
      },
    );
  }
}
