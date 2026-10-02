import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';

/// Answers intrinsic size queries with fixed values instead of asking [child].
///
/// Some shadcn widgets (ShadSlider, ShadResizablePanelGroup) lay out with a
/// LayoutBuilder, which throws when asked for its intrinsic size, e.g. inside
/// `Column(intrinsic_width=True)` or a Row with `intrinsic_height`. The sizes
/// given here are only used for those queries; actual layout still goes to
/// [child].
class FixedIntrinsics extends SingleChildRenderObjectWidget {
  final double minWidth;
  final double maxWidth;
  final double height;

  const FixedIntrinsics({
    super.key,
    required this.minWidth,
    required this.maxWidth,
    required this.height,
    required super.child,
  });

  @override
  RenderFixedIntrinsics createRenderObject(BuildContext context) =>
      RenderFixedIntrinsics(minWidth, maxWidth, height);

  @override
  void updateRenderObject(
    BuildContext context,
    RenderFixedIntrinsics renderObject,
  ) {
    renderObject
      ..minWidth = minWidth
      ..maxWidth = maxWidth
      ..height = height;
  }
}

class RenderFixedIntrinsics extends RenderProxyBox {
  RenderFixedIntrinsics(this._minWidth, this._maxWidth, this._height);

  double _minWidth;
  set minWidth(double value) {
    if (value == _minWidth) return;
    _minWidth = value;
    markNeedsLayout();
  }

  double _maxWidth;
  set maxWidth(double value) {
    if (value == _maxWidth) return;
    _maxWidth = value;
    markNeedsLayout();
  }

  double _height;
  set height(double value) {
    if (value == _height) return;
    _height = value;
    markNeedsLayout();
  }

  @override
  double computeMinIntrinsicWidth(double height) => _minWidth;

  @override
  double computeMaxIntrinsicWidth(double height) => _maxWidth;

  @override
  double computeMinIntrinsicHeight(double width) => _height;

  @override
  double computeMaxIntrinsicHeight(double width) => _height;
}
