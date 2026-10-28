import 'package:material_ui/material_ui.dart';

import '../extensions/control.dart';
import '../models/control.dart';
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

    Widget bottomAppBar = BottomAppBar(
      clipBehavior: clipBehavior,
      padding: control.getPadding("padding"),
      height: control.getDouble("height"),
      elevation: control.getDouble("elevation"),
      shape: _shiftNotch(
          control.getNotchedShape("shape", theme), control.getMargin("margin")),
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

/// Moves the notch of [shape] back under the floating action button when the
/// bar has a [margin].
///
/// The margin is applied around the bar, but `Scaffold` reports the button's
/// position relative to the whole bottom slot, so the notch would otherwise be
/// cut `margin.left` too far right and `margin.top` too far down.
NotchedShape? _shiftNotch(NotchedShape? shape, EdgeInsets? margin) {
  if (shape == null ||
      margin == null ||
      (margin.left == 0 && margin.top == 0)) {
    return shape;
  }
  return _OffsetNotchedShape(shape, Offset(-margin.left, -margin.top));
}

/// A [NotchedShape] that shifts the guest rectangle by [offset] before
/// cutting [inner]'s notch.
class _OffsetNotchedShape extends NotchedShape {
  const _OffsetNotchedShape(this.inner, this.offset);

  final NotchedShape inner;
  final Offset offset;

  @override
  Path getOuterPath(Rect host, Rect? guest) =>
      inner.getOuterPath(host, guest?.shift(offset));
}
