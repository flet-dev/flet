import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_server.dart';
import '../models/control.dart';
import '../utils/dismissible.dart';
import 'create_control.dart';
import 'error.dart';

class DismissibleControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletServer server;

  const DismissibleControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.server});

  @override
  Widget build(BuildContext context) {
    debugPrint("Dismissible build: ${control.id}");

    bool disabled = control.isDisabled || parentDisabled;
    var contentCtrls = children.where((c) => c.name == "content");

    if (contentCtrls.isEmpty) {
      return const ErrorControl("Dismissible does not have a content.");
    }

    var backgroundCtrls = children.where((c) => c.name == "background");

    var secondaryBackgroundCtrls =
        children.where((c) => c.name == "secondaryBackground");

    var dismissThresholds =
        parseDismissThresholds(control, "dismissThresholds");

    DismissDirection? direction = DismissDirection.values.firstWhere(
        (a) =>
            a.name.toLowerCase() ==
            control.attrString("dismissDirection", "")!.toLowerCase(),
        orElse: () => DismissDirection.horizontal);

    server.controlInvokeMethods[control.id] = (methodName, args) async {
      debugPrint("Dismissible.onMethod(${control.id})");
      if (methodName == "confirm_dismiss") {
        control.state["confirm_dismiss"]
            ?.complete(bool.tryParse(args["dismiss"] ?? ""));
        server.controlInvokeMethods.remove(control.id);
      }

      return null;
    };

    return constrainedControl(
        context,
        Dismissible(
            key: ValueKey<String>(control.id),
            direction: direction,
            background: backgroundCtrls.isNotEmpty
                ? createControl(control, backgroundCtrls.first.id, disabled)
                : Container(color: Colors.transparent),
            secondaryBackground: secondaryBackgroundCtrls.isNotEmpty
                ? createControl(
                    control, secondaryBackgroundCtrls.first.id, disabled)
                : Container(color: Colors.transparent),
            onDismissed: control.attrBool("onDismiss", false)!
                ? (DismissDirection direction) {
                    server.sendPageEvent(
                        eventTarget: control.id,
                        eventName: "dismiss",
                        eventData: direction.name);
                  }
                : null,
            onResize: control.attrBool("onResize", false)!
                ? () {
                    server.sendPageEvent(
                        eventTarget: control.id,
                        eventName: "resize",
                        eventData: "");
                  }
                : null,
            onUpdate: control.attrBool("onUpdate", false)!
                ? (DismissUpdateDetails details) {
                    server.sendPageEvent(
                        eventTarget: control.id,
                        eventName: "update",
                        eventData: json.encode(DismissibleUpdateEvent(
                                direction: details.direction.name,
                                previousReached: details.previousReached,
                                progress: details.progress,
                                reached: details.reached)
                            .toJson()));
                  }
                : null,
            confirmDismiss: control.attrBool("onConfirmDismiss", false)!
                ? (DismissDirection direction) {
                    debugPrint("Dismissible.confirmDismiss(${control.id})");
                    var completer = Completer<bool?>();
                    control.state["confirm_dismiss"] = completer;
                    server.sendPageEvent(
                        eventTarget: control.id,
                        eventName: "confirm_dismiss",
                        eventData: direction.name);
                    return completer.future;
                  }
                : null,
            movementDuration:
                Duration(milliseconds: control.attrInt("duration", 200)!),
            resizeDuration:
                Duration(milliseconds: control.attrInt("resizeDuration", 300)!),
            crossAxisEndOffset: control.attrDouble("crossAxisEndOffset", 0.0)!,
            dismissThresholds: dismissThresholds ?? {},
            child: createControl(control, contentCtrls.first.id, disabled)),
        parent,
        control);
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
