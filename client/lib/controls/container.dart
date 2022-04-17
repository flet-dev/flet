import 'package:flet_view/controls/create_control.dart';
import 'package:flet_view/controls/error.dart';
import 'package:flet_view/utils/colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

import '../models/control.dart';

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
    debugPrint("Icon build: ${control.id}");

    var bgColor =
        HexColor.fromString(context, control.attrString("bgColor", "")!);
    var contentCtrls = children.where((c) => c.name == "content");
    bool disabled = control.isDisabled || parentDisabled;

    if (contentCtrls.isEmpty) {
      return const ErrorControl("Container does not contain any content.");
    }

    return constrainedControl(
        Container(
            color: bgColor,
            padding: parseEdgeInsets(control, "padding"),
            margin: parseEdgeInsets(control, "margin"),
            alignment: parseAlignment(control, "alignment"),
            child: createControl(control, contentCtrls.first.id, disabled)),
        parent,
        control);
  }
}
