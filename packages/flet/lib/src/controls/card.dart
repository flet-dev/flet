import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';

enum CardVariant { elevated, filled, outlined }

class CardControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const CardControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("Card build: ${control.id}");
    bool disabled = control.isDisabled || parentDisabled;
    bool? adaptive = control.attrBool("adaptive") ?? parentAdaptive;

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    var clipBehavior = Clip.values.firstWhereOrNull(
      (e) =>
          e.name.toLowerCase() ==
          control.attrString("clipBehavior", "")!.toLowerCase(),
    );

    Widget? card;

    CardVariant variant = CardVariant.values.firstWhere(
        (v) =>
            v.name.toLowerCase() ==
            control.attrString("variant", "")!.toLowerCase(),
        orElse: () => CardVariant.elevated);

    if (variant == CardVariant.outlined) {
      card = Card.outlined(
          elevation: control.attrDouble("elevation"),
          shape: parseOutlinedBorder(control, "shape"),
          margin: parseEdgeInsets(control, "margin"),
          semanticContainer: control.attrBool("isSemanticContainer", true)!,
          borderOnForeground: control.attrBool("showBorderOnForeground", true)!,
          clipBehavior: clipBehavior,
          color: control.attrColor("color", context),
          shadowColor: control.attrColor("shadowColor", context),
          surfaceTintColor: control.attrColor("surfaceTintColor", context),
          child: contentCtrls.isNotEmpty
              ? createControl(control, contentCtrls.first.id, disabled,
                  parentAdaptive: adaptive)
              : null);
    } else if (variant == CardVariant.filled) {
      card = Card.filled(
          elevation: control.attrDouble("elevation"),
          shape: parseOutlinedBorder(control, "shape"),
          margin: parseEdgeInsets(control, "margin"),
          semanticContainer: control.attrBool("isSemanticContainer", true)!,
          borderOnForeground: control.attrBool("showBorderOnForeground", true)!,
          clipBehavior: clipBehavior,
          color: control.attrColor("color", context),
          shadowColor: control.attrColor("shadowColor", context),
          surfaceTintColor: control.attrColor("surfaceTintColor", context),
          child: contentCtrls.isNotEmpty
              ? createControl(control, contentCtrls.first.id, disabled,
                  parentAdaptive: adaptive)
              : null);
    } else {
      card = Card(
          elevation: control.attrDouble("elevation"),
          shape: parseOutlinedBorder(control, "shape"),
          margin: parseEdgeInsets(control, "margin"),
          semanticContainer: control.attrBool("isSemanticContainer", true)!,
          borderOnForeground: control.attrBool("showBorderOnForeground", true)!,
          clipBehavior: clipBehavior,
          color: control.attrColor("color", context),
          shadowColor: control.attrColor("shadowColor", context),
          surfaceTintColor: control.attrColor("surfaceTintColor", context),
          child: contentCtrls.isNotEmpty
              ? createControl(control, contentCtrls.first.id, disabled,
                  parentAdaptive: adaptive)
              : null);
    }

    return constrainedControl(context, card, parent, control);
  }
}
