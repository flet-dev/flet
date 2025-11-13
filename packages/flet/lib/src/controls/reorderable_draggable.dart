import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../widgets/error.dart';
import '../widgets/reorderable_item_scope.dart';

class ReorderableDraggableControl extends StatelessWidget {
  final Control control;

  const ReorderableDraggableControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ReorderableDraggableControl build: ${control.id}");

    var scope = ReorderableItemScope.of(context);
    var index = scope?.index;
    if (index == null) {
      return const ErrorControl(
          "ReorderableDraggable must be placed inside ReorderableListView.");
    }
    var content = control.buildWidget("content");
    if (content == null) {
      return const ErrorControl(
          "ReorderableDraggable.content must be set and visible");
    }

    return ReorderableDragStartListener(
        index: index, enabled: !control.disabled, child: content);
  }
}
