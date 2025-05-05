import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'draggable.dart';

class DragTargetEvent {
  final int srcId;
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

    return DragTarget<DraggableData>(
      builder: (
        BuildContext context,
        List<dynamic> accepted,
        List<dynamic> rejected,
      ) {
        return content;
      },
      onMove: (DragTargetDetails<DraggableData> details) {
        control.triggerEvent(
            "move",
            DragTargetEvent(
                    srcId: details.data.id,
                    x: details.offset.dx,
                    y: details.offset.dy)
                .toMap());
      },
      onWillAcceptWithDetails: (DragTargetDetails<DraggableData> details) {
        var groupMatch = details.data.group == group;
        control.triggerEvent("will_accept", {"accept": groupMatch});
        return groupMatch;
      },
      onAcceptWithDetails: (DragTargetDetails<DraggableData> details) {
        control.triggerEvent(
            "accept",
            DragTargetEvent(
                    srcId: details.data.id,
                    x: details.offset.dx,
                    y: details.offset.dy)
                .toMap());
      },
      onLeave: (DraggableData? data) {
        control.triggerEvent("leave", {"src_id", data?.id});
      },
    );
  }
}
