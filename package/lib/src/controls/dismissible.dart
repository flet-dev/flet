import 'package:collection/collection.dart';
import 'package:flet/src/utils/dismissible.dart';
import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class DismissibleControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const DismissibleControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    var server = FletAppServices.of(context).server;
    debugPrint("Dismissible build: ${control.id}");

    bool disabled = control.isDisabled || parentDisabled;
    var contentCtrls = children.where((c) => c.name == "content");

    if (contentCtrls.isEmpty) {
      return const ErrorControl("Dismissible does not have a content.");
    }

    var backgroundCtrls = children.where((c) => c.name == "background");

    var secondaryBackgroundCtrls =
        children.where((c) => c.name == "secondaryBackground");

    // SnackBarBehavior? behavior = SnackBarBehavior.values.firstWhereOrNull((a) =>
    //     a.name.toLowerCase() ==
    //     control.attrString("behavior", "")!.toLowerCase());

    var dismissThresholds =
        parseDismissThresholds(control, "dismissThresholds");

    DismissDirection? direction = DismissDirection.values.firstWhere(
        (a) =>
            a.name.toLowerCase() ==
            control.attrString("dismissDirection", "")!.toLowerCase(),
        orElse: () => DismissDirection.horizontal);

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
            onDismissed: (DismissDirection d) {
              server.sendPageEvent(
                  eventTarget: control.id, eventName: "dismiss", eventData: "");
            },
            onResize: () {
              server.sendPageEvent(
                  eventTarget: control.id, eventName: "resize", eventData: "");
            },
            onUpdate: (DismissUpdateDetails d) {
              server.sendPageEvent(
                  eventTarget: control.id, eventName: "update", eventData: "");
            },
            // confirmDismiss: // TODO: implement
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
