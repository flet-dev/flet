import 'package:flet/src/extensions/control.dart';
import 'package:flet/src/utils/events.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';
import 'package:window_manager/window_manager.dart';

import '../models/control.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class WindowDragAreaControl extends StatelessWidget {
  final Control control;

  const WindowDragAreaControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("WindowDragArea build: ${control.id}");

    var content = control.buildWidget("content");

    if (content == null) {
      return const ErrorControl(
          "WindowDragArea.content must be provided and visible");
    }

    final wda = GestureDetector(
      behavior: HitTestBehavior.translucent,
      onPanStart: (DragStartDetails details) {
        windowManager.startDragging();
        if (control.getBool("on_drag_start", false)!) {
          control.triggerEvent("drag_start", details.toMap());
        }
      },
      onPanEnd: (DragEndDetails details) {
        if (control.getBool("on_drag_end", false)!) {
          control.triggerEvent("drag_end", details.toMap());
        }
      },
      onDoubleTap: control.getBool("maximizable", true)!
          ? () async {
              final isMaximized = await windowManager.isMaximized();
              if (isMaximized) {
                windowManager.unmaximize();
              } else {
                windowManager.maximize();
              }

              // trigger event
              if (control.getBool("on_double_tap", false)!) {
                control.triggerEvent(
                    "double_tap", isMaximized ? "unmaximize" : "maximize");
              }
            }
          : null,
      child: content,
    );

    return ConstrainedControl(control: control, child: wda);
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
      onPanStart: (DragStartDetails details) {
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
