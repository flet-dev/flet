import 'dart:async';
import 'dart:convert';

import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/mouse.dart';
import 'create_control.dart';
import 'error.dart';

class InkWellControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const InkWellControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<InkWellControl> createState() => _InkWellControlState();
}

class _InkWellControlState extends State<InkWellControl> {
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
    debugPrint("InkWell build: ${widget.control.id}");

    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    void sendEvent(String eventName, dynamic eventData) {
      var d = "";
      if (eventData is String) {
        d = eventData;
      } else if (eventData is Map) {
        d = json.encode(eventData);
      }

      debugPrint("InkWell ${widget.control.id} $eventName");
      widget.backend.triggerControlEvent(widget.control.id, eventName, d);
    }

    var onHover = widget.control.attrBool("onHover", false)!;
    var onTap = widget.control.attrBool("onTap", false)!;
    var onTapDown = widget.control.attrBool("onTapDown", false)!;
    var onTapUp = widget.control.attrBool("onTapUp", false)!;
    var onSecondaryTap = widget.control.attrBool("onSecondaryTap", false)!;
    var onSecondaryTapDown =
        widget.control.attrBool("onSecondaryTapDown", false)!;
    var onSecondaryTapUp = widget.control.attrBool("onSecondaryTapUp", false)!;
    var onDoubleTap = widget.control.attrBool("onDoubleTap", false)!;

    var content = contentCtrls.isNotEmpty
        ? createControl(widget.control, contentCtrls.first.id, disabled,
            parentAdaptive:
                widget.control.attrBool("adaptive") ?? widget.parentAdaptive)
        : null;

    Widget? result = content;

    var hoverInterval = widget.control.attrInt("hoverInterval", 0)!;

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
            onDoubleTap)
        ? InkWell(
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
            onDoubleTap: onDoubleTap
                ? () {
                    sendEvent("double_tap", "");
                  }
                : null,
            child: result)
        : result;

    var mouseCursor = widget.control.attrString("mouseCursor");
    result = ((mouseCursor != null) || onHover)
        ? MouseRegion(
            cursor: parseMouseCursor(mouseCursor),
            onHover: onHover
                ? (details) {
                    handleHover(details);
                  }
                : null,
            child: result,
          )
        : result;

    if (result == null || result == content) {
      return const ErrorControl(
          "InkWell should have at least one event handler defined.");
    }

    return constrainedControl(context, result, widget.parent, widget.control);
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
