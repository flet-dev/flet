import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
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
    var clipBehavior = control.getClipBehavior("clip_behavior");
    var elevation = control.getDouble("elevation");
    var shape = control.getShape("shape", Theme.of(context));
    var margin = control.getMargin("margin");
    var isSemanticContainer = control.getBool("semantic_container", true)!;
    var showBorderOnForeground =
        control.getBool("show_border_on_foreground", true)!;
    var bgcolor = control.getColor("bgcolor", context);
    var shadowColor = control.getColor("shadow_color", context);

    Widget? card;

    CardVariant variant =
        control.getCardVariant("variant", CardVariant.elevated)!;

    if (variant == CardVariant.outlined) {
      card = Card.outlined(
          elevation: elevation,
          shape: shape,
          margin: margin,
          semanticContainer: isSemanticContainer,
          borderOnForeground: showBorderOnForeground,
          clipBehavior: clipBehavior,
          color: bgcolor,
          shadowColor: shadowColor,
          child: contentWidget);
    } else if (variant == CardVariant.filled) {
      card = Card.filled(
          elevation: elevation,
          shape: shape,
          margin: margin,
          semanticContainer: isSemanticContainer,
          borderOnForeground: showBorderOnForeground,
          clipBehavior: clipBehavior,
          color: bgcolor,
          shadowColor: shadowColor,
          child: contentWidget);
    } else {
      card = Card(
          elevation: elevation,
          shape: shape,
          margin: margin,
          semanticContainer: isSemanticContainer,
          borderOnForeground: showBorderOnForeground,
          clipBehavior: clipBehavior,
          color: bgcolor,
          shadowColor: shadowColor,
          child: contentWidget);
    }

    return ConstrainedControl(control: control, child: card);
  }
}
