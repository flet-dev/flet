import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';
import '../utils/transforms.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';

class BadgeControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const BadgeControl(
      {Key? key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Badge build: ${control.id}");

    String? label = control.attrString("label");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled)
        : null;

    var offsetDetails = parseOffset(control, "offset");

    var bgColor = HexColor.fromString(
        Theme.of(context), control.attrString("bgColor", "")!);

    var textColor = HexColor.fromString(
        Theme.of(context), control.attrString("textColor", "")!);

    bool isLabelVisible = control.attrBool("isLabelVisible", true)!;
    var largeSize = control.attrDouble("largeSize");
    var smallSize = control.attrDouble("smallSize");

    //var height = control.attrDouble("height");
    //var thickness = control.attrDouble("thickness");
    //var color = HexColor.fromString(
    //    Theme.of(context), control.attrString("color", "")!);

    return baseControl(
        context,
        Badge(
          //child: Text("Badge"),

          label: label != null ? Text(label) : null,
          isLabelVisible: isLabelVisible,
          offset: offsetDetails != null
              ? Offset(offsetDetails.x, offsetDetails.y)
              : null,
          alignment: parseAlignment(control, "alignment"),
          backgroundColor: bgColor,
          largeSize: largeSize,
          padding: parseEdgeInsets(control, "padding"),
          smallSize: smallSize,
          textColor: textColor,
          child: child,
        ),
        parent,
        control);
  }
}
