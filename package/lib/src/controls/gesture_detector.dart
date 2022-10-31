import 'dart:async';
import 'dart:convert';

import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class GestureDetectorControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const GestureDetectorControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

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

    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var ws = FletAppServices.of(context).ws;

    void sendEvent(String eventName, dynamic eventData) {
      var d = "";
      if (eventData is String) {
        d = eventData;
      } else if (eventData is Map) {
        d = json.encode(eventData);
      }

      debugPrint("GestureDetector ${widget.control.id} $eventName");
      ws.pageEventFromWeb(
          eventTarget: widget.control.id, eventName: eventName, eventData: d);
    }

    var onHover = widget.control.attrBool("onHover", false)!;
    var onEnter = widget.control.attrBool("onEnter", false)!;
    var onExit = widget.control.attrBool("onExit", false)!;
    var onTap = widget.control.attrBool("onTap", false)!;
    var onTapDown = widget.control.attrBool("onTapDown", false)!;
    var onTapUp = widget.control.attrBool("onTapUp", false)!;
    var onSecondaryTap = widget.control.attrBool("onSecondaryTap", false)!;
    var onSecondaryTapDown =
        widget.control.attrBool("onSecondaryTapDown", false)!;
    var onSecondaryTapUp = widget.control.attrBool("onSecondaryTapUp", false)!;
    var onLongPressStart = widget.control.attrBool("onLongPressStart", false)!;
    var onLongPressEnd = widget.control.attrBool("onLongPressEnd", false)!;
    var onSecondaryLongPressStart =
        widget.control.attrBool("onSecondaryLongPressStart", false)!;
    var onSecondaryLongPressEnd =
        widget.control.attrBool("onSecondaryLongPressEnd", false)!;
    var onDoubleTap = widget.control.attrBool("onDoubleTap", false)!;
    var onDoubleTapDown = widget.control.attrBool("onDoubleTapDown", false)!;
    var onHorizontalDragStart =
        widget.control.attrBool("onHorizontalDragStart", false)!;
    var onHorizontalDragUpdate =
        widget.control.attrBool("onHorizontalDragUpdate", false)!;
    var onHorizontalDragEnd =
        widget.control.attrBool("onHorizontalDragEnd", false)!;
    var onVerticalDragStart =
        widget.control.attrBool("onVerticalDragStart", false)!;
    var onVerticalDragUpdate =
        widget.control.attrBool("onVerticalDragUpdate", false)!;
    var onVerticalDragEnd =
        widget.control.attrBool("onVerticalDragEnd", false)!;
    var onPanStart = widget.control.attrBool("onPanStart", false)!;
    var onPanUpdate = widget.control.attrBool("onPanUpdate", false)!;
    var onPanEnd = widget.control.attrBool("onPanEnd", false)!;
    var onScaleStart = widget.control.attrBool("onScaleStart", false)!;
    var onScaleUpdate = widget.control.attrBool("onScaleUpdate", false)!;
    var onScaleEnd = widget.control.attrBool("onScaleEnd", false)!;
    var onMultiTap = widget.control.attrBool("onMultiTap", false)!;
    var onMultiLongPress = widget.control.attrBool("onMultiLongPress", false)!;
    var multiTapTouches = widget.control.attrInt("multiTapTouches", 0)!;

    var content = contentCtrls.isNotEmpty
        ? createControl(widget.control, contentCtrls.first.id, disabled)
        : null;

    Widget? result = content;

    var dragInterval = widget.control.attrInt("dragInterval", 0)!;

    void handlePanStart(DragStartDetails details) {
      _panX = details.localPosition.dx;
      _panY = details.localPosition.dy;
      if (onPanStart) {
        sendEvent("pan_start", {
          "kind": details.kind?.name,
          "lx": details.localPosition.dx,
          "ly": details.localPosition.dy,
          "gx": details.globalPosition.dx,
          "gy": details.globalPosition.dy,
          "ts": details.sourceTimeStamp?.inMilliseconds
        });
      }
    }

    void handlePanUpdate(DragUpdateDetails details) {
      var now = DateTime.now().millisecondsSinceEpoch;
      if (now - _panTimestamp > dragInterval) {
        _panTimestamp = now;
        var dx = details.localPosition.dx - _panX;
        var dy = details.localPosition.dy - _panY;
        _panX = details.localPosition.dx;
        _panY = details.localPosition.dy;
        sendEvent("pan_update", {
          "dx": dx,
          "dy": dy,
          "pd": details.primaryDelta,
          "lx": details.localPosition.dx,
          "ly": details.localPosition.dy,
          "gx": details.globalPosition.dx,
          "gy": details.globalPosition.dy,
          "ts": details.sourceTimeStamp?.inMilliseconds
        });
      }
    }

    void handleHorizontalDragStart(DragStartDetails details) {
      _hDragX = details.localPosition.dx;
      _hDragY = details.localPosition.dy;
      if (onHorizontalDragStart) {
        sendEvent("horizontal_drag_start", {
          "kind": details.kind?.name,
          "lx": details.localPosition.dx,
          "ly": details.localPosition.dy,
          "gx": details.globalPosition.dx,
          "gy": details.globalPosition.dy,
          "ts": details.sourceTimeStamp?.inMilliseconds
        });
      }
    }

    void handleHorizontalDragUpdate(DragUpdateDetails details) {
      var now = DateTime.now().millisecondsSinceEpoch;
      if (now - _hDragTimestamp > dragInterval) {
        _hDragTimestamp = now;
        var dx = details.localPosition.dx - _hDragX;
        var dy = details.localPosition.dy - _hDragY;
        _hDragX = details.localPosition.dx;
        _hDragY = details.localPosition.dy;
        sendEvent("horizontal_drag_update", {
          "dx": dx,
          "dy": dy,
          "pd": details.primaryDelta,
          "lx": details.localPosition.dx,
          "ly": details.localPosition.dy,
          "gx": details.globalPosition.dx,
          "gy": details.globalPosition.dy,
          "ts": details.sourceTimeStamp?.inMilliseconds
        });
      }
    }

    void handleVerticalDragStart(DragStartDetails details) {
      _vDragX = details.localPosition.dx;
      _vDragY = details.localPosition.dy;
      if (onVerticalDragStart) {
        sendEvent("vertical_drag_start", {
          "kind": details.kind?.name,
          "lx": details.localPosition.dx,
          "ly": details.localPosition.dy,
          "gx": details.globalPosition.dx,
          "gy": details.globalPosition.dy,
          "ts": details.sourceTimeStamp?.inMilliseconds
        });
      }
    }

    void handleVerticalDragUpdate(DragUpdateDetails details) {
      var now = DateTime.now().millisecondsSinceEpoch;
      if (now - _vDragTimestamp > dragInterval) {
        _vDragTimestamp = now;
        var dx = details.localPosition.dx - _vDragX;
        var dy = details.localPosition.dy - _vDragY;
        _vDragX = details.localPosition.dx;
        _vDragY = details.localPosition.dy;
        sendEvent("vertical_drag_update", {
          "dx": dx,
          "dy": dy,
          "pd": details.primaryDelta,
          "lx": details.localPosition.dx,
          "ly": details.localPosition.dy,
          "gx": details.globalPosition.dx,
          "gy": details.globalPosition.dy,
          "ts": details.sourceTimeStamp?.inMilliseconds
        });
      }
    }

    var hoverInterval = widget.control.attrInt("hoverInterval", 0)!;

    void handleEnter(PointerEnterEvent details) {
      _hoverX = details.localPosition.dx;
      _hoverY = details.localPosition.dy;
      if (onEnter) {
        sendEvent("enter", {
          "ts": details.timeStamp.inMilliseconds,
          "kind": details.kind.name,
          "gx": details.position.dx,
          "gy": details.position.dy,
          "lx": details.localPosition.dx,
          "ly": details.localPosition.dy
        });
      }
    }

    void handleHover(PointerHoverEvent details) {
      var now = DateTime.now().millisecondsSinceEpoch;
      if (now - _hoverTimestamp > hoverInterval) {
        _hoverTimestamp = now;
        var dx = details.localPosition.dx - _hoverX;
        var dy = details.localPosition.dy - _hoverY;
        _hoverX = details.localPosition.dx;
        _hoverY = details.localPosition.dy;
        sendEvent("hover", {
          "ts": details.timeStamp.inMilliseconds,
          "kind": details.kind.name,
          "gx": details.position.dx,
          "gy": details.position.dy,
          "lx": details.localPosition.dx,
          "ly": details.localPosition.dy,
          "dx": dx,
          "dy": dy,
        });
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
            onTap: onTap
                ? () {
                    sendEvent("tap", "");
                  }
                : null,
            onTapDown: onTapDown
                ? (details) {
                    sendEvent("tap_down", {
                      "kind": details.kind?.name,
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                    });
                  }
                : null,
            onTapUp: onTapUp
                ? (details) {
                    sendEvent("tap_up", {
                      "kind": details.kind.name,
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                    });
                  }
                : null,
            onSecondaryTap: onSecondaryTap
                ? () {
                    sendEvent("secondary_tap", "");
                  }
                : null,
            onSecondaryTapDown: onSecondaryTapDown
                ? (details) {
                    sendEvent("secondary_tap_down", {
                      "kind": details.kind?.name,
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                    });
                  }
                : null,
            onSecondaryTapUp: onSecondaryTapUp
                ? (details) {
                    sendEvent("secondary_tap_up", {
                      "kind": details.kind.name,
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                    });
                  }
                : null,
            onLongPressStart: onLongPressStart
                ? (details) {
                    sendEvent("long_press_start", {
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                    });
                  }
                : null,
            onLongPressEnd: onLongPressEnd
                ? (details) {
                    sendEvent("long_press_end", {
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                      "vx": details.velocity.pixelsPerSecond.dx,
                      "vy": details.velocity.pixelsPerSecond.dy
                    });
                  }
                : null,
            onSecondaryLongPressStart: onSecondaryLongPressStart
                ? (details) {
                    sendEvent("secondary_long_press_start", {
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                    });
                  }
                : null,
            onSecondaryLongPressEnd: onSecondaryLongPressEnd
                ? (details) {
                    sendEvent("secondary_long_press_end", {
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                      "vx": details.velocity.pixelsPerSecond.dx,
                      "vy": details.velocity.pixelsPerSecond.dy
                    });
                  }
                : null,
            onDoubleTap: onDoubleTap
                ? () {
                    sendEvent("double_tap", "");
                  }
                : null,
            onDoubleTapDown: onDoubleTapDown
                ? (details) {
                    sendEvent("double_tap_down", {
                      "kind": details.kind?.name,
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                    });
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
                ? (details) {
                    sendEvent("horizontal_drag_end", {
                      "pv": details.primaryVelocity,
                      "vx": details.velocity.pixelsPerSecond.dx,
                      "vy": details.velocity.pixelsPerSecond.dy
                    });
                  }
                : null,
            onVerticalDragStart: (onVerticalDragStart || onVerticalDragUpdate)
                ? handleVerticalDragStart
                : null,
            onVerticalDragUpdate: onVerticalDragUpdate
                ? (details) {
                    handleVerticalDragUpdate(details);
                  }
                : null,
            onVerticalDragEnd: onVerticalDragEnd
                ? (details) {
                    sendEvent("vertical_drag_end", {
                      "pv": details.primaryVelocity,
                      "vx": details.velocity.pixelsPerSecond.dx,
                      "vy": details.velocity.pixelsPerSecond.dy
                    });
                  }
                : null,
            onPanStart: (onPanStart || onPanUpdate) ? handlePanStart : null,
            onPanUpdate: onPanUpdate
                ? (details) {
                    handlePanUpdate(details);
                  }
                : null,
            onPanEnd: onPanEnd
                ? (details) {
                    sendEvent("pan_end", {
                      "pv": details.primaryVelocity,
                      "vx": details.velocity.pixelsPerSecond.dx,
                      "vy": details.velocity.pixelsPerSecond.dy
                    });
                  }
                : null,
            onScaleStart: onScaleStart
                ? (details) {
                    sendEvent("scale_start", {
                      "fpx": details.focalPoint.dx,
                      "fpy": details.focalPoint.dy,
                      "lfpx": details.localFocalPoint.dx,
                      "lfpy": details.localFocalPoint.dy,
                      "pc": details.pointerCount
                    });
                  }
                : null,
            onScaleUpdate: onScaleUpdate
                ? (details) {
                    sendEvent("scale_update", {
                      "fpx": details.focalPoint.dx,
                      "fpy": details.focalPoint.dy,
                      "fpdx": details.focalPointDelta.dx,
                      "fpdy": details.focalPointDelta.dy,
                      "lfpx": details.localFocalPoint.dx,
                      "lfpy": details.localFocalPoint.dy,
                      "pc": details.pointerCount,
                      "hs": details.horizontalScale,
                      "vs": details.verticalScale,
                      "s": details.scale,
                      "r": details.rotation,
                    });
                  }
                : null,
            onScaleEnd: onScaleEnd
                ? (details) {
                    sendEvent("scale_end", {
                      "pc": details.pointerCount,
                      "vx": details.velocity.pixelsPerSecond.dx,
                      "vy": details.velocity.pixelsPerSecond.dy
                    });
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
                  instance.minNumberOfTouches = 3;
                  instance.onMultiTap = (correctNumberOfTouches) {
                    if (onMultiTap) {
                      sendEvent("multi_tap", correctNumberOfTouches.toString());
                    }
                    if (onMultiLongPress) {
                      if (correctNumberOfTouches) {
                        _debounce =
                            Timer(const Duration(milliseconds: 1000), () {
                          sendEvent("multi_long_press", "");
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

    var mouseCursor = widget.control.attrString("mouseCursor");
    result = ((mouseCursor != null) || onHover || onEnter || onExit)
        ? MouseRegion(
            cursor: parseMouseCursor(mouseCursor),
            onHover: onHover
                ? (details) {
                    handleHover(details);
                  }
                : null,
            onEnter: (onEnter || onHover) ? handleEnter : null,
            onExit: onExit
                ? (details) {
                    sendEvent("exit", {
                      "ts": details.timeStamp.inMilliseconds,
                      "kind": details.kind.name,
                      "gx": details.position.dx,
                      "gy": details.position.dy,
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy
                    });
                  }
                : null,
            child: result,
          )
        : result;

    if (result == null || result == content) {
      return const ErrorControl(
          "GestureDetector should have at least one event handler defined.");
    }

    return constrainedControl(context, result, widget.parent, widget.control);
  }

  MouseCursor parseMouseCursor(String? cursor) {
    switch (cursor) {
      case "alias":
        return SystemMouseCursors.alias;
      case "allScroll":
        return SystemMouseCursors.allScroll;
      case "basic":
        return SystemMouseCursors.basic;
      case "cell":
        return SystemMouseCursors.cell;
      case "click":
        return SystemMouseCursors.click;
      case "contextMenu":
        return SystemMouseCursors.contextMenu;
      case "copy":
        return SystemMouseCursors.copy;
      case "disappearing":
        return SystemMouseCursors.disappearing;
      case "forbidden":
        return SystemMouseCursors.forbidden;
      case "grab":
        return SystemMouseCursors.grab;
      case "grabbing":
        return SystemMouseCursors.grabbing;
      case "help":
        return SystemMouseCursors.help;
      case "move":
        return SystemMouseCursors.move;
      case "noDrop":
        return SystemMouseCursors.noDrop;
      case "none":
        return SystemMouseCursors.none;
      case "precise":
        return SystemMouseCursors.precise;
      case "progress":
        return SystemMouseCursors.progress;
      case "resizeColumn":
        return SystemMouseCursors.resizeColumn;
      case "resizeDown":
        return SystemMouseCursors.resizeDown;
      case "resizeDownLeft":
        return SystemMouseCursors.resizeDownLeft;
      case "resizeDownRight":
        return SystemMouseCursors.resizeDownRight;
      case "resizeLeft":
        return SystemMouseCursors.resizeLeft;
      case "resizeLeftRight":
        return SystemMouseCursors.resizeLeftRight;
      case "resizeRight":
        return SystemMouseCursors.resizeRight;
      case "resizeRow":
        return SystemMouseCursors.resizeRow;
      case "resizeUp":
        return SystemMouseCursors.resizeUp;
      case "resizeUpDown":
        return SystemMouseCursors.resizeUpDown;
      case "resizeUpLeft":
        return SystemMouseCursors.resizeUpLeft;
      case "resizeUpLeftDownRight":
        return SystemMouseCursors.resizeUpLeftDownRight;
      case "resizeUpRight":
        return SystemMouseCursors.resizeUpRight;
      case "resizeUpRightDownLeft":
        return SystemMouseCursors.resizeUpRightDownLeft;
      case "text":
        return SystemMouseCursors.text;
      case "verticalText":
        return SystemMouseCursors.verticalText;
      case "wait":
        return SystemMouseCursors.wait;
      case "zoomIn":
        return SystemMouseCursors.zoomIn;
      case "zoomOut":
        return SystemMouseCursors.zoomOut;
      default:
        return MouseCursor.defer;
    }
  }
}

class MultiTouchGestureRecognizer extends MultiTapGestureRecognizer {
  late MultiTouchGestureRecognizerCallback onMultiTap;
  var numberOfTouches = 0;
  int minNumberOfTouches = 0;

  MultiTouchGestureRecognizer() {
    super.onTapDown = (pointer, details) => addTouch(pointer, details);
    super.onTapUp = (pointer, details) => removeTouch(pointer, details);
    super.onTapCancel = (pointer) => cancelTouch(pointer);
    super.onTap = (pointer) => captureDefaultTap(pointer);
  }

  void addTouch(int pointer, TapDownDetails details) {
    //debugPrint("Add touch: $pointer");
    numberOfTouches++;
    if (numberOfTouches == minNumberOfTouches) {
      onMultiTap(true);
      numberOfTouches = 0;
    }
  }

  void removeTouch(int pointer, TapUpDetails details) {
    onRemoveTouch(pointer);
  }

  void cancelTouch(int pointer) {
    onRemoveTouch(pointer);
  }

  void onRemoveTouch(int pointer) {
    //debugPrint("Remove touch: $pointer");
    onMultiTap(false);
    numberOfTouches = 0;
  }

  void captureDefaultTap(int pointer) {}

  @override
  set onTapDown(onTapDown) {}

  @override
  set onTapUp(onTapUp) {}

  @override
  set onTapCancel(onTapCancel) {}

  @override
  set onTap(onTap) {}
}

typedef MultiTouchGestureRecognizerCallback = void Function(
    bool correctNumberOfTouches);
