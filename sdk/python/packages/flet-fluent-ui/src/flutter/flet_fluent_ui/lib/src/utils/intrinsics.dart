import 'package:flutter/rendering.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/widgets.dart';

/// Answers intrinsic and dry layout queries for a widget that has a natural
/// size but cannot compute one without being laid out.
///
/// fluent_ui's ListTile lays out with a LayoutBuilder, which throws when asked
/// for its intrinsic size, e.g. inside `Column(intrinsic_width=True)`. This wrapper lays [child] out at its natural
/// size, remembers that size and reports it to later queries. Before the first
/// layout it reports [estimate]; when the measured size differs, it relayouts
/// on the next frame so parents pick up the real size.
class MeasuredIntrinsics extends SingleChildRenderObjectWidget {
  final Size estimate;

  const MeasuredIntrinsics({
    super.key,
    required this.estimate,
    required super.child,
  });

  @override
  RenderMeasuredIntrinsics createRenderObject(BuildContext context) =>
      RenderMeasuredIntrinsics(estimate);

  @override
  void updateRenderObject(
    BuildContext context,
    RenderMeasuredIntrinsics renderObject,
  ) {
    renderObject.estimate = estimate;
  }
}

class RenderMeasuredIntrinsics extends RenderProxyBox {
  RenderMeasuredIntrinsics(this._estimate);

  Size _estimate;
  set estimate(Size value) {
    if (value == _estimate) return;
    _estimate = value;
    if (_measured == null) markNeedsLayout();
  }

  Size? _measured;
  bool _relayoutScheduled = false;

  Size get _reported => _measured ?? _estimate;

  @override
  double computeMinIntrinsicWidth(double height) => _reported.width;

  @override
  double computeMaxIntrinsicWidth(double height) => _reported.width;

  @override
  double computeMinIntrinsicHeight(double width) => _reported.height;

  @override
  double computeMaxIntrinsicHeight(double width) => _reported.height;

  @override
  Size computeDryLayout(BoxConstraints constraints) =>
      constraints.constrain(_reported);

  @override
  void performLayout() {
    final child = this.child;
    if (child == null) {
      size = constraints.smallest;
      return;
    }
    child.layout(constraints.loosen(), parentUsesSize: true);
    size = constraints.constrain(child.size);
    if (child.size != _reported) {
      _measured = child.size;
      // Intrinsic answers given so far were based on the old size; relayout
      // after this frame so ancestors re-query and get the real one.
      if (!_relayoutScheduled) {
        _relayoutScheduled = true;
        SchedulerBinding.instance.addPostFrameCallback((_) {
          _relayoutScheduled = false;
          if (attached) markNeedsLayout();
        });
      }
    }
  }
}
