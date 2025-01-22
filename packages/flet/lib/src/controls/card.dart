import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
import 'create_control.dart';

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
    var content = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled,
            parentAdaptive: adaptive)
        : null;
    var clipBehavior = parseClip(control.attrString("clipBehavior"));
    var elevation = control.attrDouble("elevation");
    var shape = parseOutlinedBorder(control, "shape");
    var margin = parseEdgeInsets(control, "margin");
    var isSemanticContainer = control.attrBool("isSemanticContainer", true)!;
    var showBorderOnForeground =
        control.attrBool("showBorderOnForeground", true)!;
    var color = control.attrColor("color", context);
    var shadowColor = control.attrColor("shadowColor", context);
    var surfaceTintColor = control.attrColor("surfaceTintColor", context);

    Widget? card;

    CardVariant variant =
        parseCardVariant(control.attrString("variant"), CardVariant.elevated)!;

    if (variant == CardVariant.outlined) {
      card = Card.outlined(
          elevation: elevation,
          shape: shape,
          margin: margin,
          semanticContainer: isSemanticContainer,
          borderOnForeground: showBorderOnForeground,
          clipBehavior: clipBehavior,
          color: color,
          shadowColor: shadowColor,
          surfaceTintColor: surfaceTintColor,
          child: content);
    } else if (variant == CardVariant.filled) {
      card = Card.filled(
          elevation: elevation,
          shape: shape,
          margin: margin,
          semanticContainer: isSemanticContainer,
          borderOnForeground: showBorderOnForeground,
          clipBehavior: clipBehavior,
          color: color,
          shadowColor: shadowColor,
          surfaceTintColor: surfaceTintColor,
          child: content);
    } else {
      card = Card(
          elevation: elevation,
          shape: shape,
          margin: margin,
          semanticContainer: isSemanticContainer,
          borderOnForeground: showBorderOnForeground,
          clipBehavior: clipBehavior,
          color: color,
          shadowColor: shadowColor,
          surfaceTintColor: surfaceTintColor,
          child: content);
    }

    return constrainedControl(context, card, parent, control);
  }
}
