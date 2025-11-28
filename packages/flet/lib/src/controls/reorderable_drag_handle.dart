import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import '../widgets/reorderable_item_scope.dart';

class ReorderableDragHandleControl extends StatelessWidget {
  final Control control;

  const ReorderableDragHandleControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ReorderableDragHandleControl build: ${control.id}");

    var scope = ReorderableItemScope.of(context);
    var index = scope?.index;
    if (index == null) {
      return const ErrorControl(
          "ReorderableDragHandle must be placed inside ReorderableListView.");
    }
    Widget? content = control.buildWidget("content");
    if (content == null) {
      return const ErrorControl(
          "ReorderableDragHandle.content must be set and visible");
    }

    var mouseCursor = parseMouseCursor(control.getString("mouse_cursor"));

    if (mouseCursor != null) {
      content = MouseRegion(
        cursor: mouseCursor,
        child: content,
      );
    }

    return ReorderableDragStartListener(
        index: index, enabled: !control.disabled, child: content);
  }
}
