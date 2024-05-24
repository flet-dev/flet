import 'package:flutter/material.dart';
import 'package:window_manager/window_manager.dart';

import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class WindowDragAreaControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const WindowDragAreaControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("WindowDragArea build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool maximizable = control.attrBool("maximizable", true)!;
    bool disabled = control.isDisabled || parentDisabled;

    if (contentCtrls.isEmpty) {
      return const ErrorControl(
          "WindowDragArea.content must be provided and visible");
    }

    return constrainedControl(
        context,
        WindowDragArea(
            maximizable: maximizable,
            child: createControl(control, contentCtrls.first.id, disabled,
                parentAdaptive: parentAdaptive)),
        parent,
        control);
  }
}

class WindowDragArea extends StatelessWidget {
  final Widget child;
  final bool maximizable;

  const WindowDragArea(
      {super.key, required this.child, required this.maximizable});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      behavior: HitTestBehavior.translucent,
      onPanStart: (details) {
        windowManager.startDragging();
      },
      onDoubleTap: maximizable
          ? () async {
              bool isMaximized = await windowManager.isMaximized();
              if (!isMaximized) {
                windowManager.maximize();
              } else {
                windowManager.unmaximize();
              }
            }
          : null,
      child: child,
    );
  }
}
