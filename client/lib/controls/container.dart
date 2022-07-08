import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../web_socket_client.dart';
import 'create_control.dart';

class ContainerControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const ContainerControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Container build: ${control.id}");

    var bgColor = HexColor.fromString(
        Theme.of(context), control.attrString("bgColor", "")!);
    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool ink = control.attrBool("ink", false)!;
    bool onClick = control.attrBool("onclick", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    var boxDecor = BoxDecoration(
        color: bgColor,
        border: parseBorder(Theme.of(context), control, "border"),
        borderRadius: parseBorderRadius(control, "borderRadius"));

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled)
        : null;

    if (onClick && ink) {
      return constrainedControl(
          Container(
            margin: parseEdgeInsets(control, "margin"),
            child: Ink(
                child: InkWell(
                    onTap: () {
                      debugPrint("Container ${control.id} clicked!");
                      ws.pageEventFromWeb(
                          eventTarget: control.id,
                          eventName: "click",
                          eventData: control.attrs["data"] ?? "");
                    },
                    child: Container(
                      child: child,
                      padding: parseEdgeInsets(control, "padding"),
                      alignment: parseAlignment(control, "alignment"),
                    ),
                    borderRadius: parseBorderRadius(control, "borderRadius")),
                decoration: boxDecor),
          ),
          parent,
          control);
    } else {
      var container = constrainedControl(
          Container(
              padding: parseEdgeInsets(control, "padding"),
              margin: parseEdgeInsets(control, "margin"),
              alignment: parseAlignment(control, "alignment"),
              decoration: boxDecor,
              child: child),
          parent,
          control);
      if (onClick) {
        return MouseRegion(
          cursor: SystemMouseCursors.click,
          child: GestureDetector(
            child: container,
            onTap: () {
              debugPrint("Container ${control.id} clicked!");
              ws.pageEventFromWeb(
                  eventTarget: control.id,
                  eventName: "click",
                  eventData: control.attrs["data"] ?? "");
            },
          ),
        );
      } else {
        return container;
      }
    }
  }
}
