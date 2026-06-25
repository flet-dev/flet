import 'dart:async';

import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/events.dart';
import '../utils/gesture_detector.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class GestureDetectorControl extends StatefulWidget {
  final Control control;

  GestureDetectorControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<GestureDetectorControl> createState() => _GestureDetectorControlState();
}

class _GestureDetectorControlState extends State<GestureDetectorControl> {
  int _panTimestamp = DateTime.now().millisecondsSinceEpoch;
  Offset _localPan = Offset.zero;
  Offset _globalPan = Offset.zero;
  int _hDragTimestamp = DateTime.now().millisecondsSinceEpoch;
  Offset _localHorizontalDrag = Offset.zero;
  Offset _globalHorizontalDrag = Offset.zero;
  int _vDragTimestamp = DateTime.now().millisecondsSinceEpoch;
  Offset _localVerticalDrag = Offset.zero;
  Offset _globalVerticalDrag = Offset.zero;
  int _hoverTimestamp = DateTime.now().millisecondsSinceEpoch;
  Offset _localHover = Offset.zero;
  Timer? _debounce;
  bool _rightPanActive = false;
  int _rightPanTimestamp = DateTime.now().millisecondsSinceEpoch;
  Offset _rightPanStart = Offset.zero;
  TapDownDetails? _tapDownDetails;

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    _debounce?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("GestureDetector build: ${widget.control.id}");

    var content = widget.control.buildWidget("content");

    var onHover = widget.control.hasEventHandler("hover");
    var onEnter = widget.control.hasEventHandler("enter");
    var onExit = widget.control.hasEventHandler("exit");
    var onTap = widget.control.hasEventHandler("tap");
    var onTapDown = widget.control.hasEventHandler("tap_down");
    var onTapUp = widget.control.hasEventHandler("tap_up");
    var onTapMove = widget.control.hasEventHandler("tap_move");
    var onTapCancel = widget.control.hasEventHandler("tap_cancel");
    var onSecondaryTap = widget.control.hasEventHandler("secondary_tap");
    var onSecondaryTapDown =
        widget.control.hasEventHandler("secondary_tap_down");
    var onSecondaryTapUp = widget.control.hasEventHandler("secondary_tap_up");
    var onSecondaryTapCancel =
        widget.control.hasEventHandler("secondary_tap_cancel");
    var onTertiaryTapDown = widget.control.hasEventHandler("tertiary_tap_down");
    var onTertiaryTapUp = widget.control.hasEventHandler("tertiary_tap_up");
    var onTertiaryTapCancel =
        widget.control.hasEventHandler("tertiary_tap_cancel");
    var onDoubleTap = widget.control.hasEventHandler("double_tap");
    var onDoubleTapDown = widget.control.hasEventHandler("double_tap_down");
    var onDoubleTapCancel = widget.control.hasEventHandler("double_tap_cancel");
    var onLongPressDown = widget.control.hasEventHandler("long_press_down");
    var onLongPressCancel = widget.control.hasEventHandler("long_press_cancel");
    var onLongPress = widget.control.hasEventHandler("long_press");
    var onLongPressStart = widget.control.hasEventHandler("long_press_start");
    var onLongPressMoveUpdate =
        widget.control.hasEventHandler("long_press_move_update");
    var onLongPressUp = widget.control.hasEventHandler("long_press_up");
    var onLongPressEnd = widget.control.hasEventHandler("long_press_end");
    var onSecondaryLongPressDown =
        widget.control.hasEventHandler("secondary_long_press_down");
    var onSecondaryLongPressCancel =
        widget.control.hasEventHandler("secondary_long_press_cancel");
    var onSecondaryLongPress =
        widget.control.hasEventHandler("secondary_long_press");
    var onSecondaryLongPressStart =
        widget.control.hasEventHandler("secondary_long_press_start");
    var onSecondaryLongPressMoveUpdate =
        widget.control.hasEventHandler("secondary_long_press_move_update");
    var onSecondaryLongPressUp =
        widget.control.hasEventHandler("secondary_long_press_up");
    var onSecondaryLongPressEnd =
        widget.control.hasEventHandler("secondary_long_press_end");
    var onTertiaryLongPressDown =
        widget.control.hasEventHandler("tertiary_long_press_down");
    var onTertiaryLongPressCancel =
        widget.control.hasEventHandler("tertiary_long_press_cancel");
    var onTertiaryLongPress =
        widget.control.hasEventHandler("tertiary_long_press");
    var onTertiaryLongPressStart =
        widget.control.hasEventHandler("tertiary_long_press_start");
    var onTertiaryLongPressMoveUpdate =
        widget.control.hasEventHandler("tertiary_long_press_move_update");
    var onTertiaryLongPressUp =
        widget.control.hasEventHandler("tertiary_long_press_up");
    var onTertiaryLongPressEnd =
        widget.control.hasEventHandler("tertiary_long_press_end");
    var onHorizontalDragDown =
        widget.control.hasEventHandler("horizontal_drag_down");
    var onHorizontalDragStart =
        widget.control.hasEventHandler("horizontal_drag_start");
    var onHorizontalDragUpdate =
        widget.control.hasEventHandler("horizontal_drag_update");
    var onHorizontalDragEnd =
        widget.control.hasEventHandler("horizontal_drag_end");
    var onHorizontalDragCancel =
        widget.control.hasEventHandler("horizontal_drag_cancel");
    var onVerticalDragDown =
        widget.control.hasEventHandler("vertical_drag_down");
    var onVerticalDragStart =
        widget.control.hasEventHandler("vertical_drag_start");
    var onVerticalDragUpdate =
        widget.control.hasEventHandler("vertical_drag_update");
    var onVerticalDragEnd = widget.control.hasEventHandler("vertical_drag_end");
    var onVerticalDragCancel =
        widget.control.hasEventHandler("vertical_drag_cancel");
    var onPanDown = widget.control.hasEventHandler("pan_down");
    var onPanStart = widget.control.hasEventHandler("pan_start");
    var onPanUpdate = widget.control.hasEventHandler("pan_update");
    var onPanEnd = widget.control.hasEventHandler("pan_end");
    var onPanCancel = widget.control.hasEventHandler("pan_cancel");
    var onScaleStart = widget.control.hasEventHandler("scale_start");
    var onScaleUpdate = widget.control.hasEventHandler("scale_update");
    var onScaleEnd = widget.control.hasEventHandler("scale_end");
    var onForcePressStart = widget.control.hasEventHandler("force_press_start");
    var onForcePressPeak = widget.control.hasEventHandler("force_press_peak");
    var onForcePressUpdate =
        widget.control.hasEventHandler("force_press_update");
    var onForcePressEnd = widget.control.hasEventHandler("force_press_end");
    var onMultiTap = widget.control.hasEventHandler("multi_tap");
    var onMultiLongPress = widget.control.hasEventHandler("multi_long_press");
    var multiTapTouches = widget.control.getInt("multi_tap_touches", 0)!;
    var onScroll = widget.control.hasEventHandler("scroll");

    Widget? result = content;

    var dragInterval = widget.control.getInt("drag_interval", 0)!;

    void handlePanStart(DragStartDetails details) {
      _localPan = Offset(details.localPosition.dx, details.localPosition.dy);
      _globalPan = Offset(details.globalPosition.dx, details.globalPosition.dy);
      if (onPanStart) {
        widget.control.triggerEvent("pan_start", details.toMap());
      }
    }

    void handlePanUpdate(DragUpdateDetails details) {
      var now = DateTime.now().millisecondsSinceEpoch;
      if (now - _panTimestamp > dragInterval) {
        _panTimestamp = now;
        widget.control
            .triggerEvent("pan_update", details.toMap(_localPan, _globalPan));
        _localPan = details.localPosition;
      }
    }

    void handleHorizontalDragStart(DragStartDetails details) {
      _localHorizontalDrag = details.localPosition;
      _globalHorizontalDrag = details.globalPosition;
      if (onHorizontalDragStart) {
        widget.control.triggerEvent("horizontal_drag_start", details.toMap());
      }
    }

    void handleHorizontalDragUpdate(DragUpdateDetails details) {
      var now = DateTime.now().millisecondsSinceEpoch;
      if (now - _hDragTimestamp > dragInterval) {
        _hDragTimestamp = now;
        widget.control.triggerEvent("horizontal_drag_update",
            details.toMap(_localHorizontalDrag, _globalHorizontalDrag));
        _localHorizontalDrag = details.localPosition;
        _globalHorizontalDrag = details.globalPosition;
      }
    }

    void handleVerticalDragStart(DragStartDetails details) {
      _localVerticalDrag = details.localPosition;
      _globalVerticalDrag = details.globalPosition;
      if (onVerticalDragStart) {
        widget.control.triggerEvent("vertical_drag_start", details.toMap());
      }
    }

    void handleVerticalDragUpdate(DragUpdateDetails details) {
      var now = DateTime.now().millisecondsSinceEpoch;
      if (now - _vDragTimestamp > dragInterval) {
        _vDragTimestamp = now;
        widget.control.triggerEvent("vertical_drag_update",
            details.toMap(_localVerticalDrag, _globalVerticalDrag));
        _localVerticalDrag = details.localPosition;
        _globalVerticalDrag = details.globalPosition;
      }
    }

    var hoverInterval = widget.control.getInt("hover_interval", 0)!;

    void handleEnter(PointerEnterEvent details) {
      _localHover = details.localPosition;
      if (onEnter) {
        widget.control.triggerEvent("enter", details.toMap());
      }
    }

    void handleHover(PointerHoverEvent details) {
      var now = DateTime.now().millisecondsSinceEpoch;
      if (now - _hoverTimestamp > hoverInterval) {
        _hoverTimestamp = now;
        widget.control.triggerEvent("hover", details.toMap(_localHover));
        _localHover = details.localPosition;
      }
    }

    result = (onTap |
            onTapDown |
            onTapUp |
            onTapMove |
            onTapCancel |
            onSecondaryTap |
            onSecondaryTapDown |
            onSecondaryTapUp |
            onSecondaryTapCancel |
            onTertiaryTapDown |
            onTertiaryTapUp |
            onTertiaryTapCancel |
            onDoubleTap |
            onDoubleTapDown |
            onDoubleTapCancel |
            onLongPressDown |
            onLongPressCancel |
            onLongPress |
            onLongPressStart |
            onLongPressMoveUpdate |
            onLongPressUp |
            onLongPressEnd |
            onSecondaryLongPressDown |
            onSecondaryLongPressCancel |
            onSecondaryLongPress |
            onSecondaryLongPressStart |
            onSecondaryLongPressMoveUpdate |
            onSecondaryLongPressUp |
            onSecondaryLongPressEnd |
            onTertiaryLongPressDown |
            onTertiaryLongPressCancel |
            onTertiaryLongPress |
            onTertiaryLongPressStart |
            onTertiaryLongPressMoveUpdate |
            onTertiaryLongPressUp |
            onTertiaryLongPressEnd |
            onHorizontalDragDown |
            onHorizontalDragStart |
            onHorizontalDragUpdate |
            onHorizontalDragEnd |
            onHorizontalDragCancel |
            onVerticalDragDown |
            onVerticalDragStart |
            onVerticalDragUpdate |
            onVerticalDragEnd |
            onVerticalDragCancel |
            onPanDown |
            onPanStart |
            onPanUpdate |
            onPanEnd |
            onPanCancel |
            onScaleStart |
            onScaleUpdate |
            onScaleEnd |
            onForcePressStart |
            onForcePressPeak |
            onForcePressUpdate |
            onForcePressEnd)
        ? GestureDetector(
            behavior: HitTestBehavior.translucent,
            excludeFromSemantics:
                widget.control.getBool("exclude_from_semantics", false)!,
            trackpadScrollCausesScale:
                widget.control.getBool("trackpad_scroll_causes_scale", false)!,
            supportedDevices: () {
              var supportedDevices =
                  widget.control.get<List<String?>>("allowed_devices");
              return supportedDevices
                  ?.map((d) => parsePointerDeviceKind(d))
                  .nonNulls
                  .toSet();
            }(),
            onTap: onTap
                ? () =>
                    widget.control.triggerEvent("tap", _tapDownDetails?.toMap())
                : null,
            onTapDown: onTapDown || onTap
                ? (TapDownDetails details) {
                    _tapDownDetails = details;
                    if (onTapDown) {
                      widget.control.triggerEvent("tap_down", details.toMap());
                    }
                  }
                : null,
            onTapUp: onTapUp
                ? (TapUpDetails details) {
                    widget.control.triggerEvent("tap_up", details.toMap());
                  }
                : null,
            onTapMove: onTapMove
                ? (TapMoveDetails details) {
                    widget.control.triggerEvent("tap_move", details.toMap());
                  }
                : null,
            onTapCancel: onTapCancel
                ? () {
                    widget.control.triggerEvent("tap_cancel");
                  }
                : null,
            onSecondaryTap: onSecondaryTap
                ? () => widget.control.triggerEvent("secondary_tap")
                : null,
            onSecondaryTapDown: onSecondaryTapDown
                ? (TapDownDetails details) {
                    widget.control
                        .triggerEvent("secondary_tap_down", details.toMap());
                  }
                : null,
            onSecondaryTapUp: onSecondaryTapUp
                ? (TapUpDetails details) {
                    widget.control
                        .triggerEvent("secondary_tap_up", details.toMap());
                  }
                : null,
            onSecondaryTapCancel: onSecondaryTapCancel
                ? () {
                    widget.control.triggerEvent("secondary_tap_cancel");
                  }
                : null,
            onTertiaryTapDown: onTertiaryTapDown
                ? (TapDownDetails details) {
                    widget.control
                        .triggerEvent("tertiary_tap_down", details.toMap());
                  }
                : null,
            onTertiaryTapUp: onTertiaryTapUp
                ? (TapUpDetails details) {
                    widget.control
                        .triggerEvent("tertiary_tap_up", details.toMap());
                  }
                : null,
            onTertiaryTapCancel: onTertiaryTapCancel
                ? () {
                    widget.control.triggerEvent("tertiary_tap_cancel");
                  }
                : null,
            onLongPressDown: onLongPressDown
                ? (LongPressDownDetails details) {
                    widget.control
                        .triggerEvent("long_press_down", details.toMap());
                  }
                : null,
            onLongPressCancel: onLongPressCancel
                ? () {
                    widget.control.triggerEvent("long_press_cancel");
                  }
                : null,
            onLongPress: onLongPress
                ? () {
                    widget.control.triggerEvent("long_press");
                  }
                : null,
            onLongPressStart: onLongPressStart
                ? (LongPressStartDetails details) {
                    widget.control
                        .triggerEvent("long_press_start", details.toMap());
                  }
                : null,
            onLongPressMoveUpdate: onLongPressMoveUpdate
                ? (LongPressMoveUpdateDetails details) {
                    widget.control.triggerEvent(
                        "long_press_move_update", details.toMap());
                  }
                : null,
            onLongPressUp: onLongPressUp
                ? () {
                    widget.control.triggerEvent("long_press_up");
                  }
                : null,
            onLongPressEnd: onLongPressEnd
                ? (LongPressEndDetails details) {
                    widget.control
                        .triggerEvent("long_press_end", details.toMap());
                  }
                : null,
            onSecondaryLongPressDown: onSecondaryLongPressDown
                ? (LongPressDownDetails details) {
                    widget.control.triggerEvent(
                        "secondary_long_press_down", details.toMap());
                  }
                : null,
            onSecondaryLongPressCancel: onSecondaryLongPressCancel
                ? () {
                    widget.control.triggerEvent("secondary_long_press_cancel");
                  }
                : null,
            onSecondaryLongPress: onSecondaryLongPress
                ? () {
                    widget.control.triggerEvent("secondary_long_press");
                  }
                : null,
            onSecondaryLongPressStart: onSecondaryLongPressStart
                ? (LongPressStartDetails details) {
                    widget.control.triggerEvent(
                        "secondary_long_press_start", details.toMap());
                  }
                : null,
            onSecondaryLongPressMoveUpdate: onSecondaryLongPressMoveUpdate
                ? (LongPressMoveUpdateDetails details) {
                    widget.control.triggerEvent(
                        "secondary_long_press_move_update", details.toMap());
                  }
                : null,
            onSecondaryLongPressUp: onSecondaryLongPressUp
                ? () {
                    widget.control.triggerEvent("secondary_long_press_up");
                  }
                : null,
            onSecondaryLongPressEnd: onSecondaryLongPressEnd
                ? (LongPressEndDetails details) {
                    widget.control.triggerEvent(
                        "secondary_long_press_end", details.toMap());
                  }
                : null,
            onTertiaryLongPressDown: onTertiaryLongPressDown
                ? (LongPressDownDetails details) {
                    widget.control.triggerEvent(
                        "tertiary_long_press_down", details.toMap());
                  }
                : null,
            onTertiaryLongPressCancel: onTertiaryLongPressCancel
                ? () {
                    widget.control.triggerEvent("tertiary_long_press_cancel");
                  }
                : null,
            onTertiaryLongPress: onTertiaryLongPress
                ? () {
                    widget.control.triggerEvent("tertiary_long_press");
                  }
                : null,
            onTertiaryLongPressStart: onTertiaryLongPressStart
                ? (LongPressStartDetails details) {
                    widget.control.triggerEvent(
                        "tertiary_long_press_start", details.toMap());
                  }
                : null,
            onTertiaryLongPressMoveUpdate: onTertiaryLongPressMoveUpdate
                ? (LongPressMoveUpdateDetails details) {
                    widget.control.triggerEvent(
                        "tertiary_long_press_move_update", details.toMap());
                  }
                : null,
            onTertiaryLongPressUp: onTertiaryLongPressUp
                ? () {
                    widget.control.triggerEvent("tertiary_long_press_up");
                  }
                : null,
            onTertiaryLongPressEnd: onTertiaryLongPressEnd
                ? (LongPressEndDetails details) {
                    widget.control.triggerEvent(
                        "tertiary_long_press_end", details.toMap());
                  }
                : null,
            onDoubleTap: onDoubleTap
                ? () => widget.control.triggerEvent("double_tap")
                : null,
            onDoubleTapDown: onDoubleTapDown
                ? (TapDownDetails details) {
                    widget.control
                        .triggerEvent("double_tap_down", details.toMap());
                  }
                : null,
            onDoubleTapCancel: onDoubleTapCancel
                ? () {
                    widget.control.triggerEvent("double_tap_cancel");
                  }
                : null,
            onHorizontalDragDown: onHorizontalDragDown
                ? (DragDownDetails details) {
                    widget.control
                        .triggerEvent("horizontal_drag_down", details.toMap());
                  }
                : null,
            onHorizontalDragStart:
                (onHorizontalDragStart || onHorizontalDragUpdate)
                    ? handleHorizontalDragStart
                    : null,
            onHorizontalDragUpdate: onHorizontalDragUpdate
                ? (details) {
                    handleHorizontalDragUpdate(details);
                  }
                : null,
            onHorizontalDragEnd: onHorizontalDragEnd
                ? (DragEndDetails details) {
                    widget.control
                        .triggerEvent("horizontal_drag_end", details.toMap());
                  }
                : null,
            onHorizontalDragCancel: onHorizontalDragCancel
                ? () {
                    widget.control.triggerEvent("horizontal_drag_cancel");
                  }
                : null,
            onVerticalDragDown: onVerticalDragDown
                ? (DragDownDetails details) {
                    widget.control
                        .triggerEvent("vertical_drag_down", details.toMap());
                  }
                : null,
            onVerticalDragStart: (onVerticalDragStart || onVerticalDragUpdate)
                ? handleVerticalDragStart
                : null,
            onVerticalDragUpdate: onVerticalDragUpdate
                ? (details) => handleVerticalDragUpdate(details)
                : null,
            onVerticalDragEnd: onVerticalDragEnd
                ? (details) {
                    widget.control
                        .triggerEvent("vertical_drag_end", details.toMap());
                  }
                : null,
            onVerticalDragCancel: onVerticalDragCancel
                ? () {
                    widget.control.triggerEvent("vertical_drag_cancel");
                  }
                : null,
            onPanDown: onPanDown
                ? (DragDownDetails details) {
                    widget.control.triggerEvent("pan_down", details.toMap());
                  }
                : null,
            onPanStart: (onPanStart || onPanUpdate) ? handlePanStart : null,
            onPanUpdate: onPanUpdate
                ? (details) {
                    handlePanUpdate(details);
                  }
                : null,
            onPanEnd: onPanEnd
                ? (DragEndDetails details) {
                    widget.control.triggerEvent("pan_end", details.toMap());
                  }
                : null,
            onPanCancel: onPanCancel
                ? () {
                    widget.control.triggerEvent("pan_cancel");
                  }
                : null,
            onForcePressStart: onForcePressStart
                ? (ForcePressDetails details) {
                    widget.control
                        .triggerEvent("force_press_start", details.toMap());
                  }
                : null,
            onForcePressPeak: onForcePressPeak
                ? (ForcePressDetails details) {
                    widget.control
                        .triggerEvent("force_press_peak", details.toMap());
                  }
                : null,
            onForcePressUpdate: onForcePressUpdate
                ? (ForcePressDetails details) {
                    widget.control
                        .triggerEvent("force_press_update", details.toMap());
                  }
                : null,
            onForcePressEnd: onForcePressEnd
                ? (ForcePressDetails details) {
                    widget.control
                        .triggerEvent("force_press_end", details.toMap());
                  }
                : null,
            onScaleStart: onScaleStart
                ? (ScaleStartDetails details) {
                    widget.control.triggerEvent("scale_start", details.toMap());
                  }
                : null,
            onScaleUpdate: onScaleUpdate
                ? (ScaleUpdateDetails details) {
                    widget.control
                        .triggerEvent("scale_update", details.toMap());
                  }
                : null,
            onScaleEnd: onScaleEnd
                ? (ScaleEndDetails details) {
                    widget.control.triggerEvent("scale_end", details.toMap());
                  }
                : null,
            child: result)
        : result;

    result = (onMultiTap || onMultiLongPress)
        ? RawGestureDetector(
            behavior: HitTestBehavior.translucent,
            gestures: {
              MultiTouchGestureRecognizer: GestureRecognizerFactoryWithHandlers<
                  MultiTouchGestureRecognizer>(
                () => MultiTouchGestureRecognizer(),
                (MultiTouchGestureRecognizer instance) {
                  instance.minNumberOfTouches = multiTapTouches;
                  instance.onMultiTap = (correctNumberOfTouches) {
                    if (onMultiTap) {
                      widget.control.triggerEvent(
                          "multi_tap", {"ct": correctNumberOfTouches});
                    }
                    if (onMultiLongPress) {
                      if (correctNumberOfTouches) {
                        _debounce =
                            Timer(const Duration(milliseconds: 1000), () {
                          widget.control.triggerEvent("multi_long_press");
                        });
                      } else if (_debounce?.isActive ?? false) {
                        _debounce!.cancel();
                      }
                    }
                  };
                },
              ),
            },
            child: result,
          )
        : result;

    var onRightPanStart = widget.control.hasEventHandler("right_pan_start");
    var onRightPanUpdate = widget.control.hasEventHandler("right_pan_update");
    var onRightPanEnd = widget.control.hasEventHandler("right_pan_end");

    if (onScroll || onRightPanStart || onRightPanUpdate || onRightPanEnd) {
      result = Listener(
        behavior: HitTestBehavior.translucent,
        onPointerSignal: onScroll
            ? (details) {
                if (details is PointerScrollEvent) {
                  widget.control.triggerEvent("scroll", details.toMap());
                }
              }
            : null,
        onPointerDown: onRightPanStart
            ? (event) {
                if (event.kind == PointerDeviceKind.mouse &&
                    event.buttons == kSecondaryMouseButton) {
                  _rightPanActive = true;
                  _rightPanStart = event.localPosition;
                  widget.control.triggerEvent("right_pan_start", event.toMap());
                }
              }
            : null,
        onPointerMove: onRightPanUpdate
            ? (event) {
                if (_rightPanActive && event.buttons == kSecondaryMouseButton) {
                  var now = DateTime.now().millisecondsSinceEpoch;
                  if (now - _rightPanTimestamp > dragInterval) {
                    _rightPanTimestamp = now;
                    widget.control.triggerEvent(
                        "right_pan_update", event.toMap(_rightPanStart));
                    _rightPanStart = event.localPosition;
                  }
                }
              }
            : null,
        onPointerUp: onRightPanEnd
            ? (event) {
                if (_rightPanActive) {
                  _rightPanActive = false;
                  widget.control.triggerEvent("right_pan_end", event.toMap());
                }
              }
            : null,
        child: result,
      );
    }

    var mouseCursor = widget.control.getMouseCursor("mouse_cursor");
    result = ((mouseCursor != null) || onHover || onEnter || onExit)
        ? MouseRegion(
            cursor: mouseCursor ?? MouseCursor.defer,
            onHover: onHover ? (details) => handleHover(details) : null,
            onEnter: (onEnter || onHover) ? handleEnter : null,
            onExit: onExit
                ? (PointerExitEvent details) {
                    widget.control.triggerEvent("exit", details.toMap());
                  }
                : null,
            child: result,
          )
        : result;

    if (result == null || result == content) {
      return const ErrorControl(
          "GestureDetector should have at least one event handler defined");
    }

    return LayoutControl(control: widget.control, child: result);
  }
}
