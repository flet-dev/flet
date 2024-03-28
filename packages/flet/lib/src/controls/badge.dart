import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/edge_insets.dart';
import '../utils/text.dart';
import '../utils/transforms.dart';
import 'create_control.dart';

class BadgeControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const BadgeControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("Badge build: ${control.id}");

    String? label = control.attrString("labelText");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled,
            parentAdaptive: parentAdaptive)
        : null;

    var offsetDetails = parseOffset(control, "offset");

    var bgColor = control.attrColor("bgcolor", context);

    var textColor = control.attrColor("textColor", context);

    bool isLabelVisible = control.attrBool("isLabelVisible", true)!;
    var largeSize = control.attrDouble("largeSize");
    var smallSize = control.attrDouble("smallSize");

    return baseControl(
        context,
        Badge(
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
          textStyle: parseTextStyle(Theme.of(context), control, "textStyle"),
          child: child,
        ),
        parent,
        control);
  }
}
