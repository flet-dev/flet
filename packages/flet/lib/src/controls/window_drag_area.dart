import 'dart:async';

import 'package:flet/src/extensions/control.dart';
import 'package:flet/src/utils/events.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:window_manager/window_manager.dart';

import '../models/control.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class WindowDragAreaControl extends StatefulWidget {
  final Control control;

  const WindowDragAreaControl({super.key, required this.control});

  @override
  State<WindowDragAreaControl> createState() => _WindowDragAreaControlState();
}

class _WindowDragAreaControlState extends State<WindowDragAreaControl> {
  /// Timestamp of the last tap-up event, used for double-tap detection.
  DateTime? _lastTapUpTime;

  /// Position of the last tap-up event, used for double-tap detection.
  Offset? _lastTapUpPosition;

  /// Whether double-tap-to-maximize behavior is enabled.
  bool get _maximizable => widget.control.getBool("maximizable", true)!;

  /// Called when the user presses down inside the drag area.
  ///
  /// If a recent tap-up occurred close in time and space (within Flutter’s
  /// [kDoubleTapTimeout] and [kDoubleTapSlop]), this is treated as a double-tap
  /// and triggers a maximize/unmaximize toggle.
  void _handlePointerDown(PointerDownEvent event) {
    if (!_maximizable || _lastTapUpTime == null) return;

    final now = DateTime.now();
    final timeDiff = now.difference(_lastTapUpTime!);
    final posDiff = (event.position - _lastTapUpPosition!).distance;

    // If tap timing and distance match Flutter's double-tap thresholds
    // — treat this as a double-tap.
    if (timeDiff <= kDoubleTapTimeout && posDiff <= kDoubleTapSlop) {
      _resetDoubleTapState();
      unawaited(_toggleMaximize());
    }
  }

  /// Called when the user lifts their finger or mouse button.
  ///
  /// Records the time and position so the next pointer down can detect
  /// a double-tap sequence.
  void _handlePointerUp(PointerUpEvent event) {
    if (!_maximizable) return;
    _lastTapUpTime = DateTime.now();
    _lastTapUpPosition = event.position;
  }

  /// Clears any stored double-tap tracking information.
  void _resetDoubleTapState() {
    _lastTapUpTime = null;
    _lastTapUpPosition = null;
  }

  /// Toggles between maximized and restored window states.
  Future<void> _toggleMaximize() async {
    final isMaximized = await windowManager.isMaximized();

    if (isMaximized) {
      await windowManager.unmaximize();
    } else {
      await windowManager.maximize();
    }

    widget.control
        .triggerEvent("double_tap", isMaximized ? "unmaximize" : "maximize");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("WindowDragArea build: ${widget.control.id}");

    final content = widget.control.buildWidget("content");
    if (content == null) {
      return const ErrorControl(
          "WindowDragArea.content must be provided and visible");
    }

    Widget dragArea = GestureDetector(
      behavior: HitTestBehavior.translucent,
      onPanStart: (DragStartDetails details) {
        // Start moving the window.
        windowManager.startDragging();

        widget.control.triggerEvent("drag_start", details.toMap());
      },
      onPanEnd: (DragEndDetails details) {
        widget.control.triggerEvent("drag_end", details.toMap());
      },
      child: content,
    );

    // If maximization is enabled, wrap with a listener to detect double-taps.
    // Using a [Listener] instead of the above [GestureDetector] ensures the
    // widget doesn’t block or consume gestures from its children.
    if (_maximizable) {
      dragArea = Listener(
        behavior: HitTestBehavior.translucent,
        onPointerDown: _handlePointerDown,
        onPointerUp: _handlePointerUp,
        onPointerCancel: (_) => _resetDoubleTapState(),
        child: dragArea,
      );
    }

    return LayoutControl(control: widget.control, child: dragArea);
  }
}
