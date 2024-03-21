import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/gradient.dart';
import '../utils/text.dart';
import 'create_control.dart';

class TooltipControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const TooltipControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("Tooltip build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    var showDuration = control.attrInt("showDuration");
    var waitDuration = control.attrInt("waitDuration");

    var bgColor = control.attrString("bgColor");
    var border = parseBorder(Theme.of(context), control, "border");
    var borderRadius = parseBorderRadius(control, "borderRadius");
    var gradient = parseGradient(Theme.of(context), control, "gradient");
    var shape = BoxShape.values.firstWhereOrNull((e) =>
        e.name.toLowerCase() == control.attrString("shape", "")!.toLowerCase());

    var defaultDecoration = TooltipTheme.of(context).decoration ??
        BoxDecoration(
          color: Colors.grey[700]!.withOpacity(0.9),
          borderRadius: const BorderRadius.all(Radius.circular(4)),
        );

    BoxDecoration? decoration;
    if (bgColor != null ||
        border != null ||
        borderRadius != null ||
        gradient != null ||
        shape != null) {
      decoration = (defaultDecoration as BoxDecoration).copyWith(
          color: control.attrColor("bgColor", context),
          gradient: gradient,
          border: border,
          borderRadius: borderRadius,
          shape: shape ?? BoxShape.rectangle);
    }

    return baseControl(
        context,
        Tooltip(
            decoration: decoration,
            enableFeedback: control.attrBool("enableFeedback"),
            enableTapToDismiss: control.attrBool("enableTapToDismiss", true)!,
            excludeFromSemantics: control.attrBool("excludeFromSemantics"),
            height: control.attrDouble("height"),
            margin: parseEdgeInsets(control, "margin"),
            padding: parseEdgeInsets(control, "padding"),
            preferBelow: control.attrBool("preferBelow"),
            message: control.attrString("message"),
            showDuration: showDuration != null
                ? Duration(milliseconds: showDuration)
                : null,
            waitDuration: waitDuration != null
                ? Duration(milliseconds: waitDuration)
                : null,
            verticalOffset: control.attrDouble("verticalOffset"),
            textStyle: parseTextStyle(Theme.of(context), control, "textStyle"),
            textAlign: parseTextAlign(control.attrString("textAlign", "")!),
            child: contentCtrls.isNotEmpty
                ? createControl(control, contentCtrls.first.id, disabled,
                    parentAdaptive: parentAdaptive)
                : null),
        parent,
        control);
  }
}
