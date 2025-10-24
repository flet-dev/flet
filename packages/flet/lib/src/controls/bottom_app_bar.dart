import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class BottomAppBarControl extends StatelessWidget {
  final Control control;

  const BottomAppBarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("BottomAppBarControl build: ${control.id}");

    final theme = Theme.of(context);
    final textDirection = Directionality.maybeOf(context) ?? TextDirection.ltr;
    var borderRadius = control.getBorderRadius("border_radius") ??
        _borderRadiusFromNotchedShape(
            theme.bottomAppBarTheme.shape, textDirection);
    final clipBehavior = control.getClipBehavior(
        "clip_behavior",
        borderRadius != null && borderRadius != BorderRadius.zero
            ? Clip.antiAlias
            : Clip.none)!;

    NotchedShape? shape = control.getNotchedShape("shape", theme);

    if (borderRadius != null && borderRadius != BorderRadius.zero) {
      shape = AutomaticNotchedShape(
        RoundedRectangleBorder(borderRadius: borderRadius),
        shape is AutomaticNotchedShape ? shape.guest : null,
      );
    }

    Widget bottomAppBar = BottomAppBar(
      clipBehavior: clipBehavior,
      padding: control.getPadding("padding"),
      height: control.getDouble("height"),
      elevation: control.getDouble("elevation"),
      shape: shape,
      shadowColor: control.getColor("shadow_color", context),
      color: control.getColor("bgcolor", context),
      notchMargin: control.getDouble("notch_margin", 4.0)!,
      child: control.buildWidget("content"),
    );

    if (borderRadius != null && borderRadius != BorderRadius.zero) {
      bottomAppBar = ClipRRect(
        borderRadius: borderRadius,
        // can't use Clip.none here, so fallback to Clip.antiAlias in that case
        clipBehavior: clipBehavior == Clip.none ? Clip.antiAlias : clipBehavior,
        child: bottomAppBar,
      );
    }

    return LayoutControl(control: control, child: bottomAppBar);
  }
}

BorderRadius? _borderRadiusFromNotchedShape(
    NotchedShape? shape, TextDirection textDirection) {
  return shape is AutomaticNotchedShape
      ? _borderRadiusFromShapeBorder(shape.host, textDirection)
      : null;
}

BorderRadius? _borderRadiusFromShapeBorder(
    ShapeBorder? shape, TextDirection textDirection) {
  if (shape is RoundedRectangleBorder) {
    return shape.borderRadius.resolve(textDirection);
  } else if (shape is ContinuousRectangleBorder) {
    return shape.borderRadius.resolve(textDirection);
  } else if (shape is BeveledRectangleBorder) {
    return shape.borderRadius.resolve(textDirection);
  }
  return null;
}
