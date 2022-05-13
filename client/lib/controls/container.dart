import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
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

    var bgColor =
        HexColor.fromString(context, control.attrString("bgColor", "")!);
    var contentCtrls = children.where((c) => c.name == "content");
    bool disabled = control.isDisabled || parentDisabled;

    return constrainedControl(
        Container(
            padding: parseEdgeInsets(control, "padding"),
            margin: parseEdgeInsets(control, "margin"),
            alignment: parseAlignment(control, "alignment"),
            decoration: BoxDecoration(
                color: bgColor,
                border: parseBorder(context, control, "border"),
                borderRadius: parseBorderRadius(control, "borderRadius")),
            child: contentCtrls.isNotEmpty
                ? createControl(control, contentCtrls.first.id, disabled)
                : null),
        parent,
        control);
  }
}
