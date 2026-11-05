import 'package:flutter/foundation.dart' show ValueListenable;
import 'package:material_ui/material_ui.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class BottomAppBarControl extends StatelessWidget {
  final Control control;

  const BottomAppBarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("BottomAppBarControl build: ${control.id}");

    final theme = Theme.of(context);
    var borderRadius = control.getBorderRadius("border_radius");
    final clipBehavior = control.getClipBehavior(
        "clip_behavior",
        borderRadius != null && borderRadius != BorderRadius.zero
            ? Clip.antiAlias
            : Clip.none)!;
    final shape = control.getNotchedShape(
        "shape", theme, BottomAppBarTheme.of(context).shape);
    final geometry =
        Scaffold.maybeOf(context) != null ? Scaffold.geometryOf(context) : null;
    final skipProps = control.internals?["skip_properties"] as List?;
    final margin = skipProps?.contains("margin") == true
        ? null
        : control.getMargin("margin");
    final marginAnimation = control.getAnimation("animate_margin");
    final content = control.buildWidget("content");

    Widget buildBar(EdgeInsets? margin, Widget? child) {
      Widget bar = BottomAppBar(
        clipBehavior: clipBehavior,
        padding: control.getPadding("padding"),
        height: control.getDouble("height"),
        elevation: control.getDouble("elevation"),
        shape: _shiftNotch(shape, margin, geometry),
        shadowColor: control.getColor("shadow_color", context),
        color: control.getColor("bgcolor", context),
        notchMargin: control.getDouble("notch_margin", 4.0)!,
        child: child,
      );
      if (borderRadius != null && borderRadius != BorderRadius.zero) {
        bar = ClipRRect(
          borderRadius: borderRadius,
          // can't use Clip.none here, so fallback to Clip.antiAlias in that case
          clipBehavior:
              clipBehavior == Clip.none ? Clip.antiAlias : clipBehavior,
          child: bar,
        );
      }
      return bar;
    }

    // LayoutControl animates an animated margin around the bar, which moves
    // the bar without resizing it, so BottomAppBar keeps its notch where it
    // was first cut. Animating the same margin here rebuilds the notch for
    // every frame of that animation. The clip is built inside the builder,
    // so adding or removing a border radius keeps the animation running.
    final bottomAppBar = margin != null && marginAnimation != null
        ? TweenAnimationBuilder<EdgeInsets>(
            tween: EdgeInsetsTween(begin: margin, end: margin),
            duration: marginAnimation.duration,
            curve: marginAnimation.curve,
            builder: (context, margin, child) => buildBar(margin, child),
            child: content,
          )
        : buildBar(margin, content);

    return LayoutControl(control: control, child: bottomAppBar);
  }
}

/// Moves the notch of [shape] back under the floating action button when the
/// bar has a [margin].
///
/// The margin is applied around the bar, but `Scaffold` reports the button's
/// position relative to the whole bottom slot, so the notch would otherwise be
/// cut `margin.left` too far right and `margin.top` too far down.
NotchedShape? _shiftNotch(NotchedShape? shape, EdgeInsets? margin,
    ValueListenable<ScaffoldGeometry>? geometry) {
  if (shape == null ||
      margin == null ||
      (margin.left == 0 && margin.top == 0)) {
    return shape;
  }
  return _OffsetNotchedShape(shape, margin, geometry);
}

/// A [NotchedShape] that shifts the guest rectangle by [margin] before
/// cutting [inner]'s notch.
///
/// Outside the bottom slot, such as in the page body, BottomAppBar measures
/// the bar's own top, which already includes `margin.top`, so only the
/// horizontal shift applies there.
class _OffsetNotchedShape extends NotchedShape {
  const _OffsetNotchedShape(this.inner, this.margin, this.geometry);

  final NotchedShape inner;
  final EdgeInsets margin;
  final ValueListenable<ScaffoldGeometry>? geometry;

  @override
  Path getOuterPath(Rect host, Rect? guest) {
    // Read while BottomAppBar cuts the notch, as it reads the same geometry.
    final inBottomSlot = geometry?.value.bottomNavigationBarTop != null;
    final offset = Offset(-margin.left, inBottomSlot ? -margin.top : 0);
    return inner.getOuterPath(host, guest?.shift(offset));
  }
}
