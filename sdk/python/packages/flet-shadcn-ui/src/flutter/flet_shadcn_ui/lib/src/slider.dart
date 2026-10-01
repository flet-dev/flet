import 'dart:math';

import 'package:flet/flet.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadSliderControl extends StatefulWidget {
  final Control control;

  const ShadSliderControl({super.key, required this.control});

  @override
  State<ShadSliderControl> createState() => _ShadSliderControlState();
}

class _ShadSliderControlState extends State<ShadSliderControl> {
  late final ShadSliderController _controller;

  @override
  void initState() {
    super.initState();
    _controller = ShadSliderController(
      initialValue: widget.control.getDouble("value", 0)!,
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _onChanged(double value) {
    widget.control.updateProperties({"value": value});
    widget.control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadSlider build: ${widget.control.id}");

    final control = widget.control;

    final value = control.getDouble("value", 0)!;
    if (_controller.value != value) {
      _controller.value = value;
    }

    final slider = ShadSlider(
      controller: _controller,
      enabled: !control.disabled,
      min: control.getDouble("min", 0),
      max: control.getDouble("max", 1),
      divisions: control.getInt("divisions"),
      thumbColor: control.getColor("thumb_color", context),
      activeTrackColor: control.getColor("active_track_color", context),
      inactiveTrackColor: control.getColor("inactive_track_color", context),
      onChanged: _onChanged,
      onChangeStart: control.hasEventHandler("change_start")
          ? (value) => control.triggerEvent("change_start", value)
          : null,
      onChangeEnd: control.hasEventHandler("change_end")
          ? (value) => control.triggerEvent("change_end", value)
          : null,
    );

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        Builder(
          builder: (context) {
            final sliderTheme = ShadTheme.of(context).sliderTheme;
            final thumbDiameter = (sliderTheme.thumbRadius ?? 10) * 2;
            return _SliderIntrinsics(
              minWidth: thumbDiameter,
              maxWidth: _preferredTrackWidth + thumbDiameter,
              height: max(sliderTheme.trackHeight ?? 8, thumbDiameter),
              child: slider,
            );
          },
        ),
      ),
    );
  }
}

/// Track width ShadSlider prefers when nothing constrains it, matching
/// Flutter's Material slider.
const double _preferredTrackWidth = 144;

/// Answers intrinsic size queries for ShadSlider.
///
/// ShadSlider lays out with a LayoutBuilder, which throws when asked for its
/// intrinsic size, e.g. inside `Column(intrinsic_width=True)` or a Row with
/// `intrinsic_height`. The sizes reported here are only used for those
/// queries; actual layout still goes to the slider.
class _SliderIntrinsics extends SingleChildRenderObjectWidget {
  final double minWidth;
  final double maxWidth;
  final double height;

  const _SliderIntrinsics({
    required this.minWidth,
    required this.maxWidth,
    required this.height,
    required super.child,
  });

  @override
  _RenderSliderIntrinsics createRenderObject(BuildContext context) =>
      _RenderSliderIntrinsics(minWidth, maxWidth, height);

  @override
  void updateRenderObject(
    BuildContext context,
    _RenderSliderIntrinsics renderObject,
  ) {
    renderObject
      ..minWidth = minWidth
      ..maxWidth = maxWidth
      ..height = height;
  }
}

class _RenderSliderIntrinsics extends RenderProxyBox {
  _RenderSliderIntrinsics(this._minWidth, this._maxWidth, this._height);

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
