import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';
import '../utils/transforms.dart';

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

    String label = control.attrString("label", "")!;

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled)
        : null;

    var offsetDetails = parseOffset(control, "offset");

    //var height = control.attrDouble("height");
    //var thickness = control.attrDouble("thickness");
    //var color = HexColor.fromString(
    //    Theme.of(context), control.attrString("color", "")!);

    return baseControl(
        context,
        Badge(
          //child: Text("Badge"),

          label: Text(label),
          offset: offsetDetails != null
              ? Offset(offsetDetails.x, offsetDetails.y)
              : null,
          child: child,
        ),
        parent,
        control);
  }
}
