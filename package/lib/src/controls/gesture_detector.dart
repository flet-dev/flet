import 'dart:convert';

import 'package:flet/src/flet_app_services.dart';
import 'package:flutter/material.dart';

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

    return baseControl(
        context,
        GestureDetector(
            onTap: control.attrBool("onTap", false)!
                ? () {
                    sendEvent("tap", "");
                  }
                : null,
            onTapDown: control.attrBool("onTapDown", false)!
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
            child: contentCtrls.isNotEmpty
                ? createControl(control, contentCtrls.first.id, disabled)
                : null),
        parent,
        control);
  }
}
