import 'dart:async';

import 'package:flet/src/utils/events.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
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
  double _panX = 0;
  double _panY = 0;
  int _hDragTimestamp = DateTime.now().millisecondsSinceEpoch;
  double _hDragX = 0;
  double _hDragY = 0;
  int _vDragTimestamp = DateTime.now().millisecondsSinceEpoch;
  double _vDragX = 0;
  double _vDragY = 0;
  int _hoverTimestamp = DateTime.now().millisecondsSinceEpoch;
  double _hoverX = 0;
  double _hoverY = 0;
  Timer? _debounce;

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

    var onHover = widget.control.getBool("on_hover", false)!;
    var onEnter = widget.control.getBool("on_enter", false)!;
    var onExit = widget.control.getBool("on_exit", false)!;
    var onTap = widget.control.getBool("on_tap", false)!;
    var onTapDown = widget.control.getBool("on_tap_down", false)!;
    var onTapUp = widget.control.getBool("on_tap_up", false)!;
    var onSecondaryTap = widget.control.getBool("on_secondary_tap", false)!;
    var onSecondaryTapDown =
        widget.control.getBool("on_secondary_tap_down", false)!;
    var onSecondaryTapUp =
        widget.control.getBool("on_secondary_tap_up", false)!;
    var onLongPressStart =
        widget.control.getBool("on_long_press_start", false)!;
    var onLongPressEnd = widget.control.getBool("on_long_press_end", false)!;
    var onSecondaryLongPressStart =
        widget.control.getBool("on_secondary_long_press_start", false)!;
    var onSecondaryLongPressEnd =
        widget.control.getBool("on_secondary_long_press_end", false)!;
    var onDoubleTap = widget.control.getBool("on_double_tap", false)!;
    var onDoubleTapDown = widget.control.getBool("on_double_tap_down", false)!;
    var onHorizontalDragStart =
        widget.control.getBool("on_horizontal_drag_start", false)!;
    var onHorizontalDragUpdate =
        widget.control.getBool("on_horizontal_drag_update", false)!;
    var onHorizontalDragEnd =
        widget.control.getBool("on_horizontal_drag_end", false)!;
    var onVerticalDragStart =
        widget.control.getBool("on_vertical_drag_start", false)!;
    var onVerticalDragUpdate =
        widget.control.getBool("on_vertical_drag_update", false)!;
    var onVerticalDragEnd =
        widget.control.getBool("on_vertical_drag_end", false)!;
    var onPanStart = widget.control.getBool("on_pan_start", false)!;
    var onPanUpdate = widget.control.getBool("on_pan_update", false)!;
    var onPanEnd = widget.control.getBool("on_pan_end", false)!;
    var onScaleStart = widget.control.getBool("on_scale_start", false)!;
    var onScaleUpdate = widget.control.getBool("on_scale_update", false)!;
    var onScaleEnd = widget.control.getBool("on_scale_end", false)!;
    var onMultiTap = widget.control.getBool("on_multi_tap", false)!;
    var onMultiLongPress =
        widget.control.getBool("on_multi_long_press", false)!;
    var multiTapTouches = widget.control.getInt("multi_tap_touches", 0)!;
    var onScroll = widget.control.getBool("on_scroll", false)!;

    Widget? result = content;

    var dragInterval = widget.control.getInt("drag_interval", 0)!;

    void handlePanStart(DragStartDetails details) {
      _panX = details.localPosition.dx;
      _panY = details.localPosition.dy;
      if (onPanStart) {
        widget.control.triggerEvent("pan_start", details.toMap());
      }
    }

    void handlePanUpdate(DragUpdateDetails details) {
      var now = DateTime.now().millisecondsSinceEpoch;
      if (now - _panTimestamp > dragInterval) {
        _panTimestamp = now;
        widget.control.triggerEvent("pan_update", details.toMap(_panX, _panY));
        _panX = details.localPosition.dx;
        _panY = details.localPosition.dy;
      }
    }

    void handleHorizontalDragStart(DragStartDetails details) {
      _hDragX = details.localPosition.dx;
      _hDragY = details.localPosition.dy;
      if (onHorizontalDragStart) {
        widget.control.triggerEvent("horizontal_drag_start", details.toMap());
      }
    }

    void handleHorizontalDragUpdate(DragUpdateDetails details) {
      var now = DateTime.now().millisecondsSinceEpoch;
      if (now - _hDragTimestamp > dragInterval) {
        _hDragTimestamp = now;
        widget.control.triggerEvent(
            "horizontal_drag_update", details.toMap(_hDragX, _hDragY));
        _hDragX = details.localPosition.dx;
        _hDragY = details.localPosition.dy;
      }
    }

    void handleVerticalDragStart(DragStartDetails details) {
      _vDragX = details.localPosition.dx;
      _vDragY = details.localPosition.dy;
      if (onVerticalDragStart) {
        widget.control.triggerEvent("vertical_drag_start", details.toMap());
      }
    }

    void handleVerticalDragUpdate(DragUpdateDetails details) {
      var now = DateTime.now().millisecondsSinceEpoch;
      if (now - _vDragTimestamp > dragInterval) {
        _vDragTimestamp = now;
        widget.control.triggerEvent(
            "vertical_drag_update", details.toMap(_vDragX, _vDragY));
        _vDragX = details.localPosition.dx;
        _vDragY = details.localPosition.dy;
      }
    }

    var hoverInterval = widget.control.getInt("hover_interval", 0)!;

    void handleEnter(PointerEnterEvent details) {
      _hoverX = details.localPosition.dx;
      _hoverY = details.localPosition.dy;
      if (onEnter) {
        widget.control.triggerEvent("enter", details.toMap());
      }
    }

    void handleHover(PointerHoverEvent details) {
      var now = DateTime.now().millisecondsSinceEpoch;
      if (now - _hoverTimestamp > hoverInterval) {
        _hoverTimestamp = now;
        widget.control.triggerEvent("hover", details.toMap(_hoverX, _hoverY));
        _hoverX = details.localPosition.dx;
        _hoverY = details.localPosition.dy;
      }
    }

    result = (onTap |
            onTapDown |
            onTapUp |
            onSecondaryTap |
            onSecondaryTapDown |
            onSecondaryTapUp |
            onLongPressStart |
            onLongPressEnd |
            onSecondaryLongPressStart |
            onSecondaryLongPressEnd |
            onDoubleTap |
            onDoubleTapDown |
            onHorizontalDragStart |
            onHorizontalDragUpdate |
            onHorizontalDragEnd |
            onVerticalDragStart |
            onVerticalDragUpdate |
            onVerticalDragEnd |
            onPanStart |
            onPanUpdate |
            onPanEnd |
            onScaleStart |
            onScaleUpdate |
            onScaleEnd)
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
            onTap: onTap ? () => widget.control.triggerEvent("tap") : null,
            onTapDown: onTapDown
                ? (TapDownDetails details) {
                    widget.control.triggerEvent("tap_down", details.toMap());
                  }
                : null,
            onTapUp: onTapUp
                ? (TapUpDetails details) {
                    widget.control.triggerEvent("tap_up", details.toMap());
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
            onLongPressStart: onLongPressStart
                ? (LongPressStartDetails details) {
                    widget.control
                        .triggerEvent("long_press_start", details.toMap());
                  }
                : null,
            onLongPressEnd: onLongPressEnd
                ? (LongPressEndDetails details) {
                    widget.control
                        .triggerEvent("long_press_end", details.toMap());
                  }
                : null,
            onSecondaryLongPressStart: onSecondaryLongPressStart
                ? (LongPressStartDetails details) {
                    widget.control.triggerEvent(
                        "secondary_long_press_start", details.toMap());
                  }
                : null,
            onSecondaryLongPressEnd: onSecondaryLongPressEnd
                ? (LongPressEndDetails details) {
                    widget.control.triggerEvent(
                        "secondary_long_press_end", details.toMap());
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

    result = onScroll
        ? Listener(
            behavior: HitTestBehavior.translucent,
            onPointerSignal: (details) {
              if (details is PointerScrollEvent) {
                widget.control.triggerEvent("scroll", details.toMap());
              }
            },
            child: result)
        : result;

    var mouseCursor =
        parseMouseCursor(widget.control.getString("mouse_cursor"));
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

    return ConstrainedControl(control: widget.control, child: result);
  }
}
