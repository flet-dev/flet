import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/edge_insets.dart';
import '../utils/gradient.dart';
import '../utils/images.dart';
import '../utils/others.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

class TooltipControl extends StatelessWidget with FletStoreMixin {
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
    return withPageArgs((context, pageArgs) {
      var decorationImage =
          parseDecorationImage(Theme.of(context), control, "image", pageArgs);
      var decoration = boxDecorationFromDetails(
        gradient: parseGradient(Theme.of(context), control, "gradient"),
        border: parseBorder(Theme.of(context), control, "border"),
        borderRadius: parseBorderRadius(control, "borderRadius",
            const BorderRadius.all(Radius.circular(4)))!,
        shape: parseBoxShape(control.attrString("shape"), BoxShape.rectangle)!,
        color: control.attrColor(
            "bgColor", context, Colors.grey[700]!.withOpacity(0.9))!,
        blendMode: parseBlendMode(control.attrString("blendMode")),
        boxShadow: parseBoxShadow(Theme.of(context), control, "shadow"),
        image: decorationImage,
      );

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
              textStyle:
                  parseTextStyle(Theme.of(context), control, "textStyle"),
              textAlign: parseTextAlign(control.attrString("textAlign")),
              child: contentCtrls.isNotEmpty
                  ? createControl(control, contentCtrls.first.id, disabled,
                      parentAdaptive: parentAdaptive)
                  : null),
          parent,
          control);
    });
  }
}
