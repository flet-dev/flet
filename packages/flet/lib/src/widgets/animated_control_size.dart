import 'dart:ui' show lerpDouble;

import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';

import '../utils/animations.dart';

/// Lays the child out at each intermediate size. A natural dimension stays
/// loose while the other dimension animates, so text and images can reflow.
class AnimatedControlSize extends StatefulWidget {
  final double? width;
  final double? height;
  final ImplicitAnimationDetails? animation;
  final VoidCallback? onEnd;
  final Widget child;

  const AnimatedControlSize({
    super.key,
    this.width,
    this.height,
    this.animation,
    this.onEnd,
    required this.child,
  });

  @override
  State<AnimatedControlSize> createState() => _AnimatedControlSizeState();
}

class _AnimatedControlSizeState extends State<AnimatedControlSize>
    with SingleTickerProviderStateMixin {
  @override
  Widget build(BuildContext context) => _SizeBox(widget, this);
}

class _SizeBox extends SingleChildRenderObjectWidget {
  final AnimatedControlSize settings;
  final TickerProvider vsync;

  _SizeBox(this.settings, this.vsync) : super(child: settings.child);

  @override
  _RenderControlSize createRenderObject(BuildContext context) =>
      _RenderControlSize(settings, vsync);

  @override
  void updateRenderObject(
      BuildContext context, _RenderControlSize renderObject) {
    renderObject.configure(settings);
  }
}

class _RenderControlSize extends RenderConstrainedBox {
  final TickerProvider vsync;
  AnimatedControlSize _settings;
  AnimationController? _controller;
  BoxConstraints? _lastParent;
  double? _lastWidth, _lastHeight;
  Size? _lastNatural;
  late Size _from;
  // A null endpoint leaves that axis under its usual layout constraints.
  double? _toWidth, _toHeight;
  double _layoutValue = 0;

  _RenderControlSize(this._settings, this.vsync)
      : super(
            additionalConstraints: BoxConstraints.tightFor(
                width: _settings.width, height: _settings.height));

  void configure(AnimatedControlSize settings) {
    final old = _settings.animation;
    _settings = settings;
    additionalConstraints =
        BoxConstraints.tightFor(width: settings.width, height: settings.height);
    if (old?.duration != settings.animation?.duration ||
        old?.curve != settings.animation?.curve) {
      markNeedsLayout();
    }
  }

  void _start() {
    // Most controls never animate. Allocate the ticker on the first transition.
    final controller = _controller ??= AnimationController(vsync: vsync)
      ..addListener(() {
        if (_controller!.value != _layoutValue) markNeedsLayout();
      })
      ..addStatusListener((status) {
        if (status == AnimationStatus.completed && attached) {
          _settings.onEnd?.call();
        }
      });
    controller.duration = _settings.animation!.duration;
    // forward(from: 0) synchronously notifies listeners during this layout.
    _layoutValue = 0;
    controller.forward(from: 0);
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  BoxConstraints _frameConstraints(BoxConstraints parent) {
    if (_controller?.isAnimating != true || _settings.animation == null) {
      return additionalConstraints.enforce(parent);
    }
    final t = _settings.animation!.curve.transform(_controller!.value);
    return parent.tighten(
      width: _toWidth == null
          ? _settings.width
          : lerpDouble(_from.width, _toWidth, t),
      height: _toHeight == null
          ? _settings.height
          : lerpDouble(_from.height, _toHeight, t),
    );
  }

  @override
  Size computeDryLayout(BoxConstraints constraints) =>
      child!.getDryLayout(_frameConstraints(constraints));

  @override
  double? computeDryBaseline(
          BoxConstraints constraints, TextBaseline baseline) =>
      child!.getDryBaseline(_frameConstraints(constraints), baseline);

  @override
  void performLayout() {
    final width = _settings.width;
    final height = _settings.height;
    final enabled =
        (_settings.animation?.duration ?? Duration.zero) > Duration.zero;
    final bothNatural = width == null && height == null;
    final widthChanged = width != _lastWidth;
    final heightChanged = height != _lastHeight;
    final parentChanged = constraints != _lastParent;
    final target = additionalConstraints.enforce(constraints);
    _layoutValue = _controller?.value ?? 0;
    if (_controller?.isAnimating != true) {
      _toWidth = _toHeight = null;
    }

    // Only an animated natural endpoint needs measurement. Use real layout
    // so children such as LayoutBuilder can resolve their size.
    Size? natural;
    if (enabled &&
        (bothNatural ||
            (width == null && (widthChanged || _toWidth != null)) ||
            (height == null && (heightChanged || _toHeight != null)))) {
      child!.layout(target, parentUsesSize: true);
      natural = child!.size;
    }

    if (!enabled ||
        (parentChanged && bothNatural && !widthChanged && !heightChanged)) {
      _controller?.stop();
      _toWidth = _toHeight = null;
    } else if (_lastParent != null) {
      // With both axes natural, a new measured size under the same parent
      // constraints comes from the content and can start a transition.
      final observeContent = bothNatural &&
          !widthChanged &&
          !heightChanged &&
          !parentChanged &&
          _lastNatural != null;
      final animateWidth = widthChanged ||
          (observeContent &&
              _toWidth == null &&
              natural!.width != _lastNatural!.width);
      final animateHeight = heightChanged ||
          (observeContent &&
              _toHeight == null &&
              natural!.height != _lastNatural!.height);
      if (animateWidth || animateHeight) {
        _from = size;
        if (animateWidth) {
          _toWidth = width == null ? natural!.width : target.minWidth;
        }
        if (animateHeight) {
          _toHeight = height == null ? natural!.height : target.minHeight;
        }
        if (_toWidth == size.width) _toWidth = null;
        if (_toHeight == size.height) _toHeight = null;
        if (_toWidth != null || _toHeight != null) {
          _start();
        } else {
          _controller?.stop();
        }
      }
      // If a natural endpoint changes in flight (e.g. image decoding), use
      // the newly measured endpoint for the rest of the transition.
      if (_toWidth != null) {
        _toWidth = width == null ? natural!.width : target.minWidth;
      }
      if (_toHeight != null) {
        _toHeight = height == null ? natural!.height : target.minHeight;
      }
    }
    _lastParent = constraints;
    _lastWidth = width;
    _lastHeight = height;
    _lastNatural = natural;

    child!.layout(_frameConstraints(constraints), parentUsesSize: true);
    size = child!.size;
  }
}
