import 'dart:convert';

import 'package:flet/src/controls/error.dart';
import 'package:flet/src/flet_app_services.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../models/control.dart';
import 'create_control.dart';

class GestureDetectorControl extends StatelessWidget {
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
  Widget build(BuildContext context) {
    debugPrint("GestureDetector build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    var ws = FletAppServices.of(context).ws;

    void sendEvent(String eventName, dynamic eventData) {
      var d = "";
      if (eventData is String) {
        d = eventData;
      } else if (eventData is Map) {
        d = json.encode(eventData);
      }

      debugPrint("GestureDetector ${control.id} $eventName");
      ws.pageEventFromWeb(
          eventTarget: control.id, eventName: eventName, eventData: d);
    }

    var onHover = control.attrBool("onHover", false)!;
    var onEnter = control.attrBool("onEnter", false)!;
    var onExit = control.attrBool("onExit", false)!;
    var onTap = control.attrBool("onTap", false)!;
    var onTapDown = control.attrBool("onTapDown", false)!;
    var onTapUp = control.attrBool("onTapUp", false)!;
    var onSecondaryTap = control.attrBool("onSecondaryTap", false)!;
    var onSecondaryTapDown = control.attrBool("onSecondaryTapDown", false)!;
    var onSecondaryTapUp = control.attrBool("onSecondaryTapUp", false)!;
    var onLongPressStart = control.attrBool("onLongPressStart", false)!;
    var onLongPressEnd = control.attrBool("onLongPressEnd", false)!;
    var onSecondaryLongPressStart =
        control.attrBool("onSecondaryLongPressStart", false)!;
    var onSecondaryLongPressEnd =
        control.attrBool("onSecondaryLongPressEnd", false)!;
    var onDoubleTap = control.attrBool("onDoubleTap", false)!;
    var onDoubleTapDown = control.attrBool("onDoubleTapDown", false)!;
    var onHorizontalDragStart =
        control.attrBool("onHorizontalDragStart", false)!;
    var onHorizontalDragUpdate =
        control.attrBool("onHorizontalDragUpdate", false)!;
    var onHorizontalDragEnd = control.attrBool("onHorizontalDragEnd", false)!;
    var onVerticalDragStart = control.attrBool("onVerticalDragStart", false)!;
    var onVerticalDragUpdate = control.attrBool("onVerticalDragUpdate", false)!;
    var onVerticalDragEnd = control.attrBool("onVerticalDragEnd", false)!;
    var onPanStart = control.attrBool("onPanStart", false)!;
    var onPanUpdate = control.attrBool("onPanUpdate", false)!;
    var onPanEnd = control.attrBool("onPanEnd", false)!;
    var onScaleStart = control.attrBool("onScaleStart", false)!;
    var onScaleUpdate = control.attrBool("onScaleUpdate", false)!;
    var onScaleEnd = control.attrBool("onScaleEnd", false)!;

    var content = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled)
        : null;

    Widget? widget;

    var gd = (onTap |
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
            onHorizontalDragStart: onHorizontalDragStart
                ? (details) {
                    sendEvent("horizontal_drag_start", {
                      "kind": details.kind?.name,
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                      "ts": details.sourceTimeStamp?.inMilliseconds
                    });
                  }
                : null,
            onHorizontalDragUpdate: onHorizontalDragUpdate
                ? (details) {
                    sendEvent("horizontal_drag_update", {
                      "dx": details.delta.dx,
                      "dy": details.delta.dy,
                      "pd": details.primaryDelta,
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                      "ts": details.sourceTimeStamp?.inMilliseconds
                    });
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
            onVerticalDragStart: onVerticalDragStart
                ? (details) {
                    sendEvent("vertical_drag_start", {
                      "kind": details.kind?.name,
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                      "ts": details.sourceTimeStamp?.inMilliseconds
                    });
                  }
                : null,
            onVerticalDragUpdate: onVerticalDragUpdate
                ? (details) {
                    sendEvent("vertical_drag_update", {
                      "dx": details.delta.dx,
                      "dy": details.delta.dy,
                      "pd": details.primaryDelta,
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                      "ts": details.sourceTimeStamp?.inMilliseconds
                    });
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
            onPanStart: onPanStart
                ? (details) {
                    sendEvent("pan_start", {
                      "kind": details.kind?.name,
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                      "ts": details.sourceTimeStamp?.inMilliseconds
                    });
                  }
                : null,
            onPanUpdate: onPanUpdate
                ? (details) {
                    sendEvent("pan_update", {
                      "dx": details.delta.dx,
                      "dy": details.delta.dy,
                      "pd": details.primaryDelta,
                      "lx": details.localPosition.dx,
                      "ly": details.localPosition.dy,
                      "gx": details.globalPosition.dx,
                      "gy": details.globalPosition.dy,
                      "ts": details.sourceTimeStamp?.inMilliseconds
                    });
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
            child: content)
        : null;

    widget = (onHover | onEnter | onExit)
        ? MouseRegion(
            cursor: parseMouseCursor(control.attrString("mouseCursor")),
            onHover: onHover
                ? (details) {
                    sendEvent("hover", {
                      "ts": details.timeStamp.inMilliseconds,
                      "kind": details.kind.name,
                      "gpx": details.position.dx,
                      "gpy": details.position.dy,
                      "lpx": details.localPosition.dx,
                      "lpy": details.localPosition.dy,
                      "gdx": details.delta.dx,
                      "gdy": details.delta.dy,
                      "ldx": details.localDelta.dx,
                      "ldy": details.localDelta.dy,
                    });
                  }
                : null,
            onEnter: onEnter
                ? (details) {
                    sendEvent("enter", {
                      "ts": details.timeStamp.inMilliseconds,
                      "kind": details.kind.name,
                      "gpx": details.position.dx,
                      "gpy": details.position.dy,
                      "lpx": details.localPosition.dx,
                      "lpy": details.localPosition.dy,
                      "gdx": details.delta.dx,
                      "gdy": details.delta.dy,
                      "ldx": details.localDelta.dx,
                      "ldy": details.localDelta.dy,
                    });
                  }
                : null,
            onExit: onExit
                ? (details) {
                    sendEvent("exit", {
                      "ts": details.timeStamp.inMilliseconds,
                      "kind": details.kind.name,
                      "gpx": details.position.dx,
                      "gpy": details.position.dy,
                      "lpx": details.localPosition.dx,
                      "lpy": details.localPosition.dy,
                      "gdx": details.delta.dx,
                      "gdy": details.delta.dy,
                      "ldx": details.localDelta.dx,
                      "ldy": details.localDelta.dy,
                    });
                  }
                : null,
            child: gd ?? content,
          )
        : gd;

    if (widget == null) {
      return const ErrorControl(
          "GestureDetector should have at least one event handler defined.");
    }

    return baseControl(context, widget, parent, control);
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
