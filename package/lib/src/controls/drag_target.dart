import 'dart:convert';

import 'error.dart';
import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import 'create_control.dart';

class DragTargetControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const DragTargetControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("DragTarget build: ${control.id}");

    var group = control.attrString("group", "");
    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled)
        : null;

    if (child == null) {
      return const ErrorControl("DragTarget should have content.");
    }

    final ws = FletAppServices.of(context).ws;

    return DragTarget<String>(
      builder: (
        BuildContext context,
        List<dynamic> accepted,
        List<dynamic> rejected,
      ) {
        debugPrint(
            "DragTarget.builder ${control.id}: accepted=${accepted.length}, rejected=${rejected.length}");
        return child;
      },
      onWillAccept: (data) {
        debugPrint("DragTarget.onAccept ${control.id}: $data");
        String srcGroup = "";
        if (data != null) {
          var jd = json.decode(data);
          srcGroup = jd["group"] as String;
        }
        var groupsEqual = srcGroup == group;
        ws.pageEventFromWeb(
            eventTarget: control.id,
            eventName: "will_accept",
            eventData:
                control.attrString("data", "")! + groupsEqual.toString());
        return groupsEqual;
      },
      onAccept: (data) {
        debugPrint("DragTarget.onAccept ${control.id}: $data");
        var jd = json.decode(data);
        var srcId = jd["id"] as String;
        ws.pageEventFromWeb(
            eventTarget: control.id,
            eventName: "accept",
            eventData: control.attrString("data", "")! + srcId);
      },
      // onAcceptWithDetails: (details) {
      //   debugPrint(
      //       "onAcceptWithDetails: ${details.data} ${details.offset}");
      // },
      onLeave: (data) {
        debugPrint("DragTarget.onLeave ${control.id}: $data");
        String srcId = "";
        if (data != null) {
          var jd = json.decode(data);
          srcId = jd["id"] as String;
        }
        ws.pageEventFromWeb(
            eventTarget: control.id,
            eventName: "leave",
            eventData: control.attrString("data", "")! + srcId);
      },
    );
  }
}
