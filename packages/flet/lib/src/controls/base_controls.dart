import 'dart:math';

import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/badge.dart';
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
    w = _tooltip(w, Theme.of(context), control);
    w = _directionality(w, control);
    return _expandable(w, control);
  }
}

class ConstrainedControl extends StatelessWidget {
  final Control control;
  final Widget child;

  const ConstrainedControl(
      {super.key, required this.control, required this.child});

  @override
  Widget build(BuildContext context) {
    Widget w = _opacity(context, child, control);
    w = _tooltip(w, Theme.of(context), control);
    w = _directionality(w, control);
    w = _sizedControl(w, control);
    w = _rotatedControl(context, w, control);
    w = _scaledControl(context, w, control);
    w = _offsetControl(context, w, control);
    w = _aspectRatio(w, control);
    w = _positionedControl(context, w, control);
    w = _badge(w, Theme.of(context), control);
    return _expandable(w, control);
  }
}

Widget _tooltip(Widget widget, ThemeData theme, Control control) {
  var tooltip = parseTooltip(control, "tooltip", widget, theme);
  return tooltip ?? widget;
}

Widget _badge(Widget widget, ThemeData theme, Control control) {
  var badge = parseBadge(control, "badge", widget, theme);
  return badge ?? widget;
}

Widget _aspectRatio(Widget widget, Control control) {
  var aspectRatio = control.getDouble("aspectRatio");
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
  var parent = control.parent;
  if (parent != null && ["view", "column", "row"].contains(parent.type)) {
    int? expand = control.getInt("expand");
    var expandLoose = control.getBool("expandLoose");
    return expand != null
        ? (expandLoose == true)
            ? Flexible(flex: expand, child: widget)
            : Expanded(flex: expand, child: widget)
        : widget;
  }
  return widget;
}

Widget _opacity(BuildContext context, Widget widget, Control control) {
  var opacity = control.getDouble("opacity");
  var animation = parseAnimation(control, "animateOpacity");
  if (animation != null) {
    return AnimatedOpacity(
      duration: animation.duration,
      curve: animation.curve,
      opacity: opacity ?? 1.0,
      onEnd: control.getBool("on_animation_end", false)!
          ? () {
              FletBackend.of(context)
                  .triggerControlEvent(control, "animation_end", "opacity");
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
  var rotationDetails = parseRotate(control, "rotate");
  var animation = parseAnimation(control, "animateRotation");
  if (animation != null) {
    return AnimatedRotation(
      turns: rotationDetails != null ? rotationDetails.angle / (2 * pi) : 0,
      alignment: rotationDetails?.alignment ?? Alignment.center,
      duration: animation.duration,
      curve: animation.curve,
      onEnd: control.getBool("on_animation_end", false)!
          ? () {
              FletBackend.of(context)
                  .triggerControlEvent(control, "animation_end", "rotation");
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
  var scaleDetails = parseScale(control, "scale");
  var animation = parseAnimation(control, "animateScale");
  if (animation != null) {
    return AnimatedScale(
      scale: scaleDetails?.scale ?? 1.0,
      alignment: scaleDetails?.alignment ?? Alignment.center,
      duration: animation.duration,
      curve: animation.curve,
      onEnd: control.getBool("on_animation_end", false)!
          ? () {
              FletBackend.of(context)
                  .triggerControlEvent(control, "animation_end", "scale");
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
  var offset = parseOffset(control, "offset");
  var animation = parseAnimation(control, "animateOffset");
  if (offset != null && animation != null) {
    return AnimatedSlide(
      offset: offset,
      duration: animation.duration,
      curve: animation.curve,
      onEnd: control.getBool("on_animation_end", false)!
          ? () {
              FletBackend.of(context)
                  .triggerControlEvent(control, "animation_end", "offset");
            }
          : null,
      child: widget,
    );
  } else if (offset != null) {
    return FractionalTranslation(translation: offset, child: widget);
  }
  return widget;
}

Widget _positionedControl(
    BuildContext context, Widget widget, Control control) {
  var left = control.getDouble("left", null);
  var top = control.getDouble("top", null);
  var right = control.getDouble("right", null);
  var bottom = control.getDouble("bottom", null);

  var animation = parseAnimation(control, "animatePosition");
  if (animation != null) {
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
      onEnd: control.getBool("on_animation_end", false)!
          ? () {
              FletBackend.of(context)
                  .triggerControlEvent(control, "animation_end", "position");
            }
          : null,
      child: widget,
    );
  } else if (left != null || top != null || right != null || bottom != null) {
    var parent = control.parent;
    if (parent?.type != "stack" && parent?.type != "page") {
      return ErrorControl("Error displaying ${control.type}",
          description:
              "Control can be positioned absolutely with \"left\", \"top\", \"right\" and \"bottom\" properties inside Stack control only.");
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
  var width = control.getDouble("width");
  var height = control.getDouble("height");
  if ((width != null || height != null) &&
      !["container", "image"].contains(control.type)) {
    widget = ConstrainedBox(
      constraints: BoxConstraints.tightFor(width: width, height: height),
      child: widget,
    );
  }
  var animation = parseAnimation(control, "animateSize");
  if (animation != null) {
    return AnimatedSize(
        duration: animation.duration, curve: animation.curve, child: widget);
  }
  return widget;
}
