import 'package:flet/src/controls/error.dart';
import 'package:flutter/material.dart';
import 'package:window_manager/window_manager.dart';

import '../models/control.dart';
import 'create_control.dart';

class WindowDragAreaControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const WindowDragAreaControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("WindowDragArea build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    if (contentCtrls.isEmpty) {
      return const ErrorControl("WindowDragArea should have content.");
    }

    return constrainedControl(
        DragToMoveArea(
            child: createControl(control, contentCtrls.first.id, disabled)),
        parent,
        control);
  }
}
