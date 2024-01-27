import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/launch_url.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_control_stateful_mixin.dart';

class CupertinoButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const CupertinoButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  State<CupertinoButtonControl> createState() => _CupertinoButtonControlState();
}

class _CupertinoButtonControlState extends State<CupertinoButtonControl>
    with FletControlStatefulMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoButton build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var contentCtrls = widget.children.where((c) => c.name == "content");
    if (contentCtrls.isEmpty) {
      return const ErrorControl(
          "CupertinoButton has no content control. Please specify one.");
    }

    bool filled = widget.control.attrBool("filled", false)!;
    double pressedOpacity = widget.control.attrDouble("opacityOnClick", 0.4)!;
    double minSize = widget.control.attrDouble("minSize", 44.0)!;
    String url = widget.control.attrString("url", "")!;
    EdgeInsets? padding = parseEdgeInsets(widget.control, "padding");
    Color disabledColor = HexColor.fromString(Theme.of(context),
            widget.control.attrString("disabledColor", "")!) ??
        CupertinoColors.quaternarySystemFill;
    Color? bgColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("bgColor", "")!);
    AlignmentGeometry alignment =
        parseAlignment(widget.control, "alignment") ?? Alignment.center;
    BorderRadius borderRadius =
        parseBorderRadius(widget.control, "borderRadius") ??
            const BorderRadius.all(Radius.circular(8.0));

    Function()? onPressed = !disabled
        ? () {
            debugPrint("Button ${widget.control.id} clicked!");
            if (url != "") {
              openWebBrowser(url,
                  webWindowName: widget.control.attrString("urlTarget"));
            }
            sendControlEvent(widget.control.id, "click", "");
          }
        : null;

    CupertinoButton? button;

    button = !filled
        ? CupertinoButton(
            onPressed: onPressed,
            disabledColor: disabledColor,
            color: bgColor,
            padding: padding,
            borderRadius: borderRadius,
            pressedOpacity: pressedOpacity,
            alignment: alignment,
            minSize: minSize,
            child:
                createControl(widget.control, contentCtrls.first.id, disabled),
          )
        : CupertinoButton.filled(
            onPressed: onPressed,
            disabledColor: disabledColor,
            padding: padding,
            borderRadius: borderRadius,
            pressedOpacity: pressedOpacity,
            alignment: alignment,
            minSize: minSize,
            child:
                createControl(widget.control, contentCtrls.first.id, disabled),
          );

    return constrainedControl(context, button, widget.parent, widget.control);
  }
}
