import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/misc.dart';
import 'base_controls.dart';
import 'control_widget.dart';

class CardControl extends StatelessWidget {
  final Control control;

  const CardControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("Card build: ${control.id}");

    var contentCtrl = control.child("content");
    var contentWidget = contentCtrl != null
        ? ControlWidget(
            control: contentCtrl,
          )
        : null;
    var clipBehavior = parseClip(control.getString("clip_behavior"));
    var elevation = control.getDouble("elevation");
    var shape = control.getOutlinedBorder("shape");
    var margin = control.getMargin("margin");
    var isSemanticContainer = control.getBool("is_semantic_container", true)!;
    var showBorderOnForeground =
        control.getBool("show_border_on_foreground", true)!;
    var color = control.getColor("color", context);
    var shadowColor = control.getColor("shadow_color", context);
    var surfaceTintColor = control.getColor("surface_tint_color", context);

    Widget? card;

    CardVariant variant =
        parseCardVariant(control.getString("variant"), CardVariant.elevated)!;

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
          child: contentWidget);
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
          child: contentWidget);
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
          child: contentWidget);
    }

    return ConstrainedControl(
      control: control,
      child: card,
    );
  }
}
