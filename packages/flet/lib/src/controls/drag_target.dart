import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'draggable.dart';

class DragTargetEvent {
  final int srcId;
  final Offset localPosition;
  final Offset globalPosition;

  DragTargetEvent({
    required this.srcId,
    required this.localPosition,
    required this.globalPosition,
  });

  Map<String, dynamic> toMap() => <String, dynamic>{
        'src_id': srcId,
        'l': {'x': localPosition.dx, 'y': localPosition.dy},
        'g': {'x': globalPosition.dx, 'y': globalPosition.dy},
      };
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

    BuildContext? dragTargetContext;

    return DragTarget<DraggableData>(
      builder: (
        BuildContext context,
        List<dynamic> accepted,
        List<dynamic> rejected,
      ) {
        dragTargetContext = context;
        return content;
      },
      onMove: (DragTargetDetails<DraggableData> details) {
        final globalPosition = details.offset;
        final localPosition =
            _getLocalPosition(dragTargetContext, globalPosition);
        control.triggerEvent(
            "move",
            DragTargetEvent(
              srcId: details.data.id,
              localPosition: localPosition,
              globalPosition: globalPosition,
            ).toMap());
      },
      onWillAcceptWithDetails: (DragTargetDetails<DraggableData> details) {
        var groupMatch = details.data.group == group;
        control.triggerEvent(
            "will_accept", {"accept": groupMatch, "src_id": details.data.id});
        return groupMatch;
      },
      onAcceptWithDetails: (DragTargetDetails<DraggableData> details) {
        final globalPosition = details.offset;
        final localPosition =
            _getLocalPosition(dragTargetContext, globalPosition);
        control.triggerEvent(
            "accept",
            DragTargetEvent(
              srcId: details.data.id,
              localPosition: localPosition,
              globalPosition: globalPosition,
            ).toMap());
      },
      onLeave: (DraggableData? data) {
        control.triggerEvent("leave", {"src_id": data?.id});
      },
    );
  }

  Offset _getLocalPosition(BuildContext? context, Offset globalPosition) {
    final renderObject = context?.findRenderObject();
    if (renderObject is! RenderBox || !renderObject.hasSize) {
      return globalPosition;
    }
    return renderObject.globalToLocal(globalPosition);
  }
}
