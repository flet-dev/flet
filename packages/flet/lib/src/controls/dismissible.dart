import 'dart:async';

import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/dismissible.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class DismissibleControl extends StatefulWidget {
  final Control control;

  DismissibleControl({Key? key, required this.control})
      : super(key: ValueKey("dismissible_${control.id}"));

  @override
  State<DismissibleControl> createState() => _DismissibleControlState();
}

class _DismissibleControlState extends State<DismissibleControl> {
  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Dismissible.$name($args)");
    switch (name) {
      case "confirm_dismiss":
        widget.control.properties
            .remove("_completer")
            ?.complete(args["dismiss"]);
      default:
        throw Exception("Unknown Dismissible method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Dismissible build: ${widget.control.id}");
    var content = widget.control.buildWidget("content");

    if (content == null) {
      return const ErrorControl("Dismissible.content must be visible");
    }

    final dismissible = Dismissible(
        key: ValueKey<int>(widget.control.id),
        direction: widget.control.getDismissDirection(
            "dismiss_direction", DismissDirection.horizontal)!,
        background: widget.control.buildWidget("background") ??
            Container(color: Colors.transparent),
        secondaryBackground:
            widget.control.buildWidget("secondary_background") ??
                Container(color: Colors.transparent),
        onDismissed: widget.control.getBool("on_dismiss", false)!
            ? (DismissDirection direction) => widget.control
                .triggerEvent("dismiss", {"direction": direction.name})
            : null,
        onResize: widget.control.getBool("on_resize", false)!
            ? () => widget.control.triggerEvent("resize")
            : null,
        onUpdate: widget.control.getBool("on_update", false)!
            ? (DismissUpdateDetails details) {
                widget.control.triggerEvent(
                    "update",
                    DismissibleUpdateEvent(
                            direction: details.direction.name,
                            previousReached: details.previousReached,
                            progress: details.progress,
                            reached: details.reached)
                        .toJson());
              }
            : null,
        confirmDismiss: widget.control.getBool("on_confirm_dismiss", false)!
            ? (DismissDirection direction) {
                var completer = Completer<bool?>();
                widget.control
                    .updateProperties({"_completer": completer}, python: false);
                widget.control.triggerEvent(
                    "confirm_dismiss", {"direction": direction.name});
                return completer.future;
              }
            : null,
        movementDuration: widget.control
            .getDuration("duration", const Duration(milliseconds: 200))!,
        resizeDuration: widget.control
            .getDuration("duration", const Duration(milliseconds: 300))!,
        crossAxisEndOffset:
            widget.control.getDouble("cross_axis_end_offset", 0.0)!,
        dismissThresholds: widget.control
            .getDismissThresholds("dismiss_thresholds", const {})!,
        child: content);

    return ConstrainedControl(control: widget.control, child: dismissible);
  }
}

class DismissibleUpdateEvent {
  final String direction;
  final bool previousReached;
  final double progress;
  final bool reached;

  DismissibleUpdateEvent(
      {required this.direction,
      required this.progress,
      required this.previousReached,
      required this.reached});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'direction': direction,
        'progress': progress,
        'reached': reached,
        'previous_reached': previousReached
      };
}
