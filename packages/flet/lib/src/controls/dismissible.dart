import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/dismissible.dart';
import 'create_control.dart';
import 'error.dart';

class DismissibleControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const DismissibleControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<DismissibleControl> createState() => _DismissibleControlState();
}

class _DismissibleControlState extends State<DismissibleControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("Dismissible build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);

    if (contentCtrls.isEmpty) {
      return const ErrorControl(
          "Dismissible.content must be provided and visible");
    }

    var backgroundCtrls =
        widget.children.where((c) => c.name == "background" && c.isVisible);

    var secondaryBackgroundCtrls = widget.children
        .where((c) => c.name == "secondaryBackground" && c.isVisible);

    var dismissThresholds =
        parseDismissThresholds(widget.control, "dismissThresholds");

    DismissDirection direction = parseDismissDirection(
        widget.control.attrString("dismissDirection"), DismissDirection.horizontal)!;

    widget.backend.subscribeMethods(widget.control.id,
        (methodName, args) async {
      debugPrint("Dismissible.onMethod(${widget.control.id})");
      if (methodName == "confirm_dismiss") {
        widget.control.state["confirm_dismiss"]
            ?.complete(bool.tryParse(args["dismiss"] ?? ""));
        widget.backend.unsubscribeMethods(widget.control.id);
      }

      return null;
    });

    return constrainedControl(
        context,
        Dismissible(
            key: ValueKey<String>(widget.control.id),
            direction: direction,
            background: backgroundCtrls.isNotEmpty
                ? createControl(
                    widget.control, backgroundCtrls.first.id, disabled,
                    parentAdaptive: adaptive)
                : Container(color: Colors.transparent),
            secondaryBackground: secondaryBackgroundCtrls.isNotEmpty
                ? createControl(
                    widget.control, secondaryBackgroundCtrls.first.id, disabled,
                    parentAdaptive: adaptive)
                : Container(color: Colors.transparent),
            onDismissed: widget.control.attrBool("onDismiss", false)!
                ? (DismissDirection direction) {
                    widget.backend.triggerControlEvent(
                        widget.control.id, "dismiss", direction.name);
                  }
                : null,
            onResize: widget.control.attrBool("onResize", false)!
                ? () {
                    widget.backend
                        .triggerControlEvent(widget.control.id, "resize");
                  }
                : null,
            onUpdate: widget.control.attrBool("onUpdate", false)!
                ? (DismissUpdateDetails details) {
                    widget.backend.triggerControlEvent(
                        widget.control.id,
                        "update",
                        json.encode(DismissibleUpdateEvent(
                                direction: details.direction.name,
                                previousReached: details.previousReached,
                                progress: details.progress,
                                reached: details.reached)
                            .toJson()));
                  }
                : null,
            confirmDismiss: widget.control.attrBool("onConfirmDismiss", false)!
                ? (DismissDirection direction) {
                    debugPrint(
                        "Dismissible.confirmDismiss(${widget.control.id})");
                    var completer = Completer<bool?>();
                    widget.control.state["confirm_dismiss"] = completer;
                    widget.backend.triggerControlEvent(
                        widget.control.id, "confirm_dismiss", direction.name);
                    return completer.future;
                  }
                : null,
            movementDuration: Duration(
                milliseconds: widget.control.attrInt("duration", 200)!),
            resizeDuration: Duration(
                milliseconds: widget.control.attrInt("resizeDuration", 300)!),
            crossAxisEndOffset:
                widget.control.attrDouble("crossAxisEndOffset", 0.0)!,
            dismissThresholds: dismissThresholds ?? {},
            child: createControl(
                widget.control, contentCtrls.first.id, disabled,
                parentAdaptive: adaptive)),
        widget.parent,
        widget.control);
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
