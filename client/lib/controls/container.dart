import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/gradient.dart';
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
    bool onLongPress = control.attrBool("onLongPress", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    var boxDecor = BoxDecoration(
        color: bgColor,
        gradient: parseGradient(Theme.of(context), control, "gradient"),
        border: parseBorder(Theme.of(context), control, "border"),
        borderRadius: parseBorderRadius(control, "borderRadius"));

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled)
        : null;

    if ((onClick || onLongPress) && ink) {
      return constrainedControl(
          Container(
            margin: parseEdgeInsets(control, "margin"),
            child: Ink(
                child: InkWell(
                    onTap: onClick
                        ? () {
                            debugPrint("Container ${control.id} clicked!");
                            ws.pageEventFromWeb(
                                eventTarget: control.id,
                                eventName: "click",
                                eventData: control.attrs["data"] ?? "");
                          }
                        : null,
                    onLongPress: onLongPress
                        ? () {
                            debugPrint("Container ${control.id} long pressed!");
                            ws.pageEventFromWeb(
                                eventTarget: control.id,
                                eventName: "long_press",
                                eventData: control.attrs["data"] ?? "");
                          }
                        : null,
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
      Widget container = Container(
          padding: parseEdgeInsets(control, "padding"),
          margin: parseEdgeInsets(control, "margin"),
          alignment: parseAlignment(control, "alignment"),
          decoration: boxDecor,
          child: child);

      if (onClick || onLongPress) {
        container = MouseRegion(
          cursor: SystemMouseCursors.click,
          child: GestureDetector(
            child: container,
            onTapDown: onClick
                ? (details) {
                    debugPrint("Container ${control.id} clicked!");
                    ws.pageEventFromWeb(
                        eventTarget: control.id,
                        eventName: "click",
                        eventData: control.attrString("data", "")! +
                            "${details.localPosition.dx}:${details.localPosition.dy} ${details.globalPosition.dx}:${details.globalPosition.dy}");
                  }
                : null,
            onLongPress: onLongPress
                ? () {
                    debugPrint("Container ${control.id} clicked!");
                    ws.pageEventFromWeb(
                        eventTarget: control.id,
                        eventName: "long_press",
                        eventData: control.attrs["data"] ?? "");
                  }
                : null,
          ),
        );
      }
      return constrainedControl(container, parent, control);
    }
  }
}
