import 'dart:async';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/animations.dart';
import '../utils/badge.dart';
import '../utils/edge_insets.dart';
import '../utils/layout.dart';
import '../utils/numbers.dart';
import '../utils/tooltip.dart';
import '../utils/transforms.dart';
import '../widgets/error.dart';

class BaseControl extends StatelessWidget {
  final Control control;
  final Widget child;

  const BaseControl({super.key, required this.control, required this.child});

  @override
  Widget build(BuildContext context) {
    Widget w = _opacity(context, child, control);
    w = _tooltip(context, w, control);
    w = _directionality(w, control);
    return _expandable(w, control);
  }
}

class LayoutControl extends StatelessWidget {
  final Control control;
  final Widget child;

  const LayoutControl({
    super.key,
    required this.control,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    Widget w = _opacity(context, child, control);
    w = _tooltip(context, w, control);
    w = _directionality(w, control);
    w = _sizedControl(w, control);
    w = _rotatedControl(context, w, control);
    w = _scaledControl(context, w, control);
    w = _offsetControl(context, w, control);
    w = _aspectRatio(w, control);
    w = _alignedControl(context, w, control);
    w = _marginControl(context, w, control);
    w = _positionedControl(context, w, control);
    w = _badge(w, Theme.of(context), control);
    w = _sizeChangeObserver(w, control);
    return _expandable(w, control);
  }
}

Widget _tooltip(BuildContext context, Widget widget, Control control) {
  final skipProps = control.internals?["skip_properties"] as List?;
  if (skipProps?.contains("tooltip") == true) return widget;

  return parseTooltip(control.get("tooltip"), context, widget) ?? widget;
}

Widget _badge(Widget widget, ThemeData theme, Control control) {
  final skipProps = control.internals?["skip_properties"] as List?;
  if (skipProps?.contains("badge") == true) return widget;

  return control.wrapWithBadge("badge", widget, theme);
}

Widget _sizeChangeObserver(Widget widget, Control control) {
  if (!control.getBool("on_size_change", false)!) return widget;

  // Opt-in size reporting to avoid extra layout work by default.
  return SizeChangeObserver(
    control: control,
    interval: control.getInt("size_change_interval", 10)!,
    child: widget,
  );
}

Widget _aspectRatio(Widget widget, Control control) {
  var aspectRatio = control.getDouble("aspect_ratio");
  return aspectRatio != null
      ? AspectRatio(aspectRatio: aspectRatio, child: widget)
      : widget;
}

Widget _directionality(Widget widget, Control control) {
  bool rtl = control.getBool("rtl", false)!;
  return rtl
      ? Directionality(textDirection: TextDirection.rtl, child: widget)
      : widget;
}

Widget _expandable(Widget widget, Control control) {
  int? expand = control.getExpand("expand");
  if (expand != null && control.parent?.internals?["host_expanded"] == true) {
    return (control.getBool("expand_loose") == true)
        ? Flexible(flex: expand, child: widget)
        : Expanded(flex: expand, child: widget);
  }
  return widget;
}

Widget _opacity(BuildContext context, Widget widget, Control control) {
  var opacity = control.getDouble("opacity");
  var animation = control.getAnimation("animate_opacity");
  if (animation != null) {
    return AnimatedOpacity(
      duration: animation.duration,
      curve: animation.curve,
      opacity: opacity ?? 1.0,
      onEnd: control.getBool("on_animation_end", false)!
          ? () {
              control.triggerEvent("animation_end", "opacity");
            }
          : null,
      child: widget,
    );
  } else if (opacity != null) {
    return Opacity(
      opacity: opacity,
      child: widget,
    );
  }
  return widget;
}

Widget _rotatedControl(BuildContext context, Widget widget, Control control) {
  var rotationDetails = control.getRotationDetails("rotate");
  var animation = control.getAnimation("animate_rotation");
  if (animation != null) {
    return AnimatedRotation(
      turns: rotationDetails != null ? rotationDetails.angle / (2 * pi) : 0,
      alignment: rotationDetails?.alignment ?? Alignment.center,
      duration: animation.duration,
      curve: animation.curve,
      onEnd: control.getBool("on_animation_end", false)!
          ? () {
              control.triggerEvent("animation_end", "rotation");
            }
          : null,
      child: widget,
    );
  } else if (rotationDetails != null) {
    return Transform.rotate(
      angle: rotationDetails.angle,
      alignment: rotationDetails.alignment,
      child: widget,
    );
  }
  return widget;
}

Widget _scaledControl(BuildContext context, Widget widget, Control control) {
  var scaleDetails = control.getScale("scale");
  var animation = control.getAnimation("animate_scale");
  if (animation != null) {
    return AnimatedScale(
      scale: scaleDetails?.scale ?? 1.0,
      alignment: scaleDetails?.alignment ?? Alignment.center,
      duration: animation.duration,
      curve: animation.curve,
      onEnd: control.getBool("on_animation_end", false)!
          ? () {
              control.triggerEvent("animation_end", "scale");
            }
          : null,
      child: widget,
    );
  } else if (scaleDetails != null) {
    return Transform.scale(
      scale: scaleDetails.scale,
      scaleX: scaleDetails.scaleX,
      scaleY: scaleDetails.scaleY,
      alignment: scaleDetails.alignment,
      child: widget,
    );
  }
  return widget;
}

Widget _offsetControl(BuildContext context, Widget widget, Control control) {
  var offset = control.getOffset("offset");
  var animation = control.getAnimation("animate_offset");
  if (offset != null && animation != null) {
    return AnimatedSlide(
      offset: offset,
      duration: animation.duration,
      curve: animation.curve,
      onEnd: control.getBool("on_animation_end", false)!
          ? () {
              control.triggerEvent("animation_end", "offset");
            }
          : null,
      child: widget,
    );
  } else if (offset != null) {
    return FractionalTranslation(translation: offset, child: widget);
  }
  return widget;
}

Widget _alignedControl(BuildContext context, Widget widget, Control control) {
  var alignment = control.getAlignment("align");
  var animation = control.getAnimation("animate_align");
  if (alignment != null && animation != null) {
    return AnimatedAlign(
      alignment: alignment,
      duration: animation.duration,
      curve: animation.curve,
      onEnd: control.getBool("on_animation_end", false)!
          ? () {
              control.triggerEvent("animation_end", "align");
            }
          : null,
      child: widget,
    );
  } else if (alignment != null) {
    return Align(
      alignment: alignment,
      child: widget,
    );
  }
  return widget;
}

Widget _marginControl(BuildContext context, Widget widget, Control control) {
  final skipProps = control.internals?["skip_properties"] as List?;
  if (skipProps?.contains("margin") == true) return widget;

  var margin = control.getEdgeInsets("margin");
  var animation = control.getAnimation("animate_margin");
  if (margin != null && animation != null) {
    return AnimatedContainer(
      margin: margin,
      duration: animation.duration,
      curve: animation.curve,
      onEnd: control.getBool("on_animation_end", false)!
          ? () {
              control.triggerEvent("animation_end", "margin");
            }
          : null,
      child: widget,
    );
  } else if (margin != null) {
    return Container(
      margin: margin,
      child: widget,
    );
  }
  return widget;
}

Widget _positionedControl(
    BuildContext context, Widget widget, Control control) {
  var left = control.getDouble("left", null);
  var top = control.getDouble("top", null);
  var right = control.getDouble("right", null);
  var bottom = control.getDouble("bottom", null);

  var errorControl = ErrorControl("Error displaying ${control.type}",
      description:
          "Control can be positioned absolutely with \"left\", \"top\", \"right\" and \"bottom\" properties inside Stack control only and page.overlay.");

  var animation = control.getAnimation("animate_position");
  if (animation != null) {
    if (control.parent?.internals?["host_positioned"] != true) {
      return errorControl;
    }
    if (left == null && top == null && right == null && bottom == null) {
      left = 0;
      top = 0;
    }

    return AnimatedPositioned(
      duration: animation.duration,
      curve: animation.curve,
      left: left,
      top: top,
      right: right,
      bottom: bottom,
      onEnd: () => control.triggerEvent("animation_end", "position"),
      child: widget,
    );
  } else if (left != null || top != null || right != null || bottom != null) {
    if (control.parent?.internals?["host_positioned"] != true) {
      return errorControl;
    }
    return Positioned(
      left: left,
      top: top,
      right: right,
      bottom: bottom,
      child: widget,
    );
  }
  return widget;
}

Widget _sizedControl(Widget widget, Control control) {
  final skipProps = control.internals?['skip_properties'] as List?;
  if (skipProps != null && ['width', 'height'].any(skipProps.contains)) {
    return widget;
  }

  final width = control.getDouble("width");
  final height = control.getDouble("height");
  final animationSize = control.getAnimation("animate_size");

  final hasFixedSize = width != null || height != null;

  if (animationSize != null) {
    return hasFixedSize
        ? AnimatedContainer(
            duration: animationSize.duration,
            curve: animationSize.curve,
            width: width,
            height: height,
            child: widget,
          )
        : AnimatedSize(
            duration: animationSize.duration,
            curve: animationSize.curve,
            child: widget,
          );
  } else {
    return hasFixedSize
        ? SizedBox(width: width, height: height, child: widget)
        : widget;
  }
}

class SizeChangeObserver extends StatefulWidget {
  final Control control;
  final int interval;
  final Widget child;

  const SizeChangeObserver({
    super.key,
    required this.control,
    required this.interval,
    required this.child,
  });

  @override
  State<SizeChangeObserver> createState() => _SizeChangeObserverState();
}

class _SizeChangeObserverState extends State<SizeChangeObserver> {
  Size? _lastSize;
  Size? _pendingSize;
  int _lastDispatch = 0;
  Timer? _timer;

  void _onSizeChanged(Size size) {
    if (!mounted || widget.control.getBool("on_size_change", false) != true) {
      return;
    }

    final now = DateTime.now().millisecondsSinceEpoch;
    final interval = widget.interval;
    final sizeChanged = _lastSize != size;

    if (!sizeChanged) {
      return;
    }

    if (_lastSize != null && interval > 0 && (now - _lastDispatch) < interval) {
      _pendingSize = size;
      _schedulePending(interval, now);
      return;
    }

    _dispatchSize(size, now);
  }

  void _dispatchSize(Size size, int now) {
    _pendingSize = null;
    _timer?.cancel();
    _lastSize = size;
    _lastDispatch = now;
    widget.control
        .triggerEvent("size_change", {"w": size.width, "h": size.height});
  }

  void _schedulePending(int interval, int now) {
    // Coalesce rapid changes into a trailing dispatch.
    _timer?.cancel();
    final remaining = interval - (now - _lastDispatch);
    final delay = Duration(milliseconds: remaining > 0 ? remaining : 0);
    _timer = Timer(delay, () {
      if (!mounted || !widget.control.getBool("on_size_change", false)!) {
        return;
      }
      final size = _pendingSize;
      if (size == null) {
        return;
      }
      _dispatchSize(size, DateTime.now().millisecondsSinceEpoch);
    });
  }

  @override
  Widget build(BuildContext context) {
    return MeasureSize(onChange: _onSizeChanged, child: widget.child);
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
}

class MeasureSize extends SingleChildRenderObjectWidget {
  final ValueChanged<Size> onChange;

  const MeasureSize({super.key, required this.onChange, required Widget child})
      : super(child: child);

  @override
  RenderObject createRenderObject(BuildContext context) {
    return _MeasureSizeRenderObject(onChange);
  }

  @override
  void updateRenderObject(
      BuildContext context, covariant RenderObject renderObject) {
    (renderObject as _MeasureSizeRenderObject).onChange = onChange;
  }
}

class _MeasureSizeRenderObject extends RenderProxyBox {
  ValueChanged<Size> onChange;
  Size? _lastSize;

  _MeasureSizeRenderObject(this.onChange);

  @override
  void performLayout() {
    super.performLayout();
    // Post-frame to avoid re-entrant layout callbacks.
    final newSize = child?.size ?? size;
    if (_lastSize == newSize) {
      return;
    }
    _lastSize = newSize;
    WidgetsBinding.instance.addPostFrameCallback((_) {
      onChange(newSize);
    });
  }
}
