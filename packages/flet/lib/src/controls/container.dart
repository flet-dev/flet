import 'package:material_ui/material_ui.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/client_actions.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/events.dart';
import '../utils/gradient.dart';
import '../utils/images.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../widgets/animated_control_size.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';

class ContainerControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const ContainerControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("Container build: ${control.id}");

    var bgColor = control.getColor("bgcolor", context);
    var content = control.buildWidget("content");
    var ink = control.getBool("ink", false)!;
    var onClick = control.hasEventHandler("click");
    var onTapDown = control.hasEventHandler("tap_down");
    var hasActions = control.hasControlActions;
    var onLongPress = control.hasEventHandler("long_press");
    var onHover = control.hasEventHandler("hover");
    var ignoreInteractions = control.getBool("ignore_interactions", false)!;
    var animation = control.getAnimation("animate");
    var blur = control.getBlur("blur");
    var colorFilter = control.getColorFilter("color_filter", Theme.of(context));
    var width = control.getDouble("width");
    var height = control.getDouble("height");
    var padding = control.getPadding("padding");
    var margin = control.getMargin("margin");
    var alignment = control.getAlignment("alignment");
    var borderRadius = control.getBorderRadius("border_radius");
    var clipBehavior = control.getClipBehavior(
        "clip_behavior", borderRadius != null ? Clip.antiAlias : Clip.none)!;
    var decorationImage = control.getDecorationImage("image", context);
    var boxDecoration = boxDecorationFromDetails(
      shape: control.getBoxShape("shape", BoxShape.rectangle)!,
      color: bgColor,
      gradient: control.getGradient("gradient", Theme.of(context)),
      borderRadius: borderRadius,
      border: control.getBorder("border", Theme.of(context),
          defaultSideColor: Colors.black),
      boxShadow: control.getBoxShadows("shadow", Theme.of(context)),
      blendMode: control.getBlendMode("blend_mode"),
      image: decorationImage,
    );
    var boxForegroundDecoration =
        control.getBoxDecoration("foreground_decoration", context);

    var sizeAnimation = control.getAnimation("animate_size");
    var onAnimationEnd = control.hasEventHandler("animation_end")
        ? () => control.triggerEvent("animation_end", "container")
        : null;
    final interactive = !control.disabled &&
        (onClick || hasActions || onLongPress || onHover || onTapDown);
    final useInk = interactive && ink;
    Widget? surfaceContent = content;
    if (useInk) {
      // Keep padding and alignment inside the InkWell so the entire box responds.
      var inkContent = animation == null
          ? Container(padding: padding, alignment: alignment, child: content)
          : AnimatedContainer(
              duration: animation.duration,
              curve: animation.curve,
              padding: padding,
              alignment: alignment,
              child: content);
      surfaceContent = Material(
          color: Colors.transparent,
          borderRadius: boxDecoration!.borderRadius,
          child: InkWell(
            // Dummy callback to enable widget
            // see https://github.com/flutter/flutter/issues/50116#issuecomment-582047374
            // and https://github.com/flutter/flutter/blob/eed80afe2c641fb14b82a22279d2d78c19661787/packages/flutter/lib/src/material/ink_well.dart#L1125-L1129
            onTap: onClick || hasActions || onTapDown
                ? () {
                    runControlActions(context, control);
                    if (onClick) {
                      control.triggerEvent("click");
                    }
                  }
                : null,
            onTapDown: onTapDown
                ? (TapDownDetails details) {
                    control.triggerEvent("tap_down", details.toMap());
                  }
                : null,
            onLongPress:
                onLongPress ? () => control.triggerEvent("long_press") : null,
            onHover: onHover
                ? (value) => control.triggerEvent("hover", value)
                : null,
            borderRadius: borderRadius,
            splashColor: control.getColor("ink_color", context),
            child: inkContent,
          ));
    }

    final surface = _ContainerSurface(
      width: width,
      height: height,
      margin: margin,
      padding: useInk ? null : padding,
      alignment: useInk ? null : alignment,
      decoration: boxDecoration,
      foregroundDecoration: boxForegroundDecoration,
      sizeAnimation: sizeAnimation,
      onSizeEnd: control.hasEventHandler("animation_end")
          ? () => control.triggerEvent("animation_end", "size")
          : null,
      clipBehavior: clipBehavior,
      child: surfaceContent,
    );
    Widget container = animation == null
        ? surface.build()
        : _AnimatedSurface(
            target: surface,
            duration: animation.duration,
            curve: animation.curve,
            onEnd: onAnimationEnd);
    if (interactive && !useInk) {
      container = MouseRegion(
        cursor: onClick || onTapDown || hasActions
            ? SystemMouseCursors.click
            : MouseCursor.defer,
        onEnter: onHover
            ? (value) {
                control.triggerEvent("hover", true);
              }
            : null,
        onExit: onHover
            ? (value) {
                control.triggerEvent("hover", false);
              }
            : null,
        child: GestureDetector(
          onTap: onClick || hasActions
              ? () {
                  runControlActions(context, control);
                  if (onClick) {
                    control.triggerEvent("click");
                  }
                }
              : null,
          onTapDown: onTapDown
              ? (TapDownDetails details) {
                  control.triggerEvent("tap_down", details.toMap());
                }
              : null,
          onLongPress: onLongPress
              ? () {
                  control.triggerEvent("long_press");
                }
              : null,
          child: container,
        ),
      );
    }

    if (blur != null) {
      container = borderRadius != null
          ? ClipRRect(
              borderRadius: borderRadius,
              child: BackdropFilter(filter: blur, child: container))
          : ClipRect(child: BackdropFilter(filter: blur, child: container));
    }
    if (colorFilter != null) {
      container = ColorFiltered(colorFilter: colorFilter, child: container);
    }

    // Always wrapped, so toggling `ignore_interactions` doesn't change the
    // tree's shape (which rebuilt the subtree, losing its state).
    container = IgnorePointer(ignoring: ignoreInteractions, child: container);

    return LayoutControl(control: control, child: container);
  }
}

// The margin is outside the dimensions. Padding, decoration, ink and clipping
// all receive the constraints for the current animation frame.
class _ContainerSurface {
  final double? width, height;
  final EdgeInsetsGeometry? margin, padding;
  final AlignmentGeometry? alignment;
  final Decoration? decoration, foregroundDecoration;
  final Clip clipBehavior;
  final ImplicitAnimationDetails? sizeAnimation;
  final VoidCallback? onSizeEnd;
  final Widget? child;

  const _ContainerSurface(
      {this.width,
      this.height,
      this.margin,
      this.padding,
      this.alignment,
      this.decoration,
      this.foregroundDecoration,
      required this.clipBehavior,
      this.sizeAnimation,
      this.onSizeEnd,
      this.child});

  Widget build({
    double? width,
    double? height,
    EdgeInsetsGeometry? margin,
    EdgeInsetsGeometry? padding,
    AlignmentGeometry? alignment,
    Decoration? decoration,
    Decoration? foregroundDecoration,
  }) {
    final sized = AnimatedControlSize(
      width: width ?? this.width,
      height: height ?? this.height,
      animation: sizeAnimation,
      onEnd: onSizeEnd,
      child: Container(
        padding: padding ?? this.padding,
        alignment: alignment ?? this.alignment,
        decoration: decoration ?? this.decoration,
        foregroundDecoration: foregroundDecoration ?? this.foregroundDecoration,
        clipBehavior: clipBehavior,
        child: child,
      ),
    );
    final outerMargin = margin ?? this.margin;
    return outerMargin == null
        ? sized
        : Padding(padding: outerMargin, child: sized);
  }
}

// All properties owned by Container.animate share one controller and one
// "container" completion, including when size and margin change together.
class _AnimatedSurface extends ImplicitlyAnimatedWidget {
  final _ContainerSurface target;

  const _AnimatedSurface(
      {required this.target,
      required super.duration,
      required super.curve,
      super.onEnd});

  @override
  AnimatedWidgetBaseState<_AnimatedSurface> createState() =>
      _AnimatedSurfaceState();
}

class _AnimatedSurfaceState extends AnimatedWidgetBaseState<_AnimatedSurface> {
  Tween<double>? _width, _height;
  EdgeInsetsGeometryTween? _margin, _padding;
  AlignmentGeometryTween? _alignment;
  DecorationTween? _decoration, _foreground;

  @override
  void forEachTween(TweenVisitor<dynamic> visitor) {
    Tween<double> dimension(dynamic value) =>
        Tween<double>(begin: value as double);
    EdgeInsetsGeometryTween inset(dynamic value) =>
        EdgeInsetsGeometryTween(begin: value as EdgeInsetsGeometry);
    DecorationTween decoration(dynamic value) =>
        DecorationTween(begin: value as Decoration);
    final target = widget.target;
    _width = visitor(_width, target.sizeAnimation == null ? target.width : null,
        dimension) as Tween<double>?;
    _height = visitor(
        _height,
        target.sizeAnimation == null ? target.height : null,
        dimension) as Tween<double>?;
    _margin =
        visitor(_margin, target.margin, inset) as EdgeInsetsGeometryTween?;
    _padding =
        visitor(_padding, target.padding, inset) as EdgeInsetsGeometryTween?;
    _alignment = visitor(
            _alignment,
            target.alignment,
            (dynamic value) =>
                AlignmentGeometryTween(begin: value as AlignmentGeometry))
        as AlignmentGeometryTween?;
    _decoration =
        visitor(_decoration, target.decoration, decoration) as DecorationTween?;
    _foreground = visitor(_foreground, target.foregroundDecoration, decoration)
        as DecorationTween?;
  }

  @override
  Widget build(BuildContext context) {
    final target = widget.target;
    return target.build(
        width: _width?.evaluate(animation),
        height: _height?.evaluate(animation),
        margin: _margin?.evaluate(animation),
        padding: _padding?.evaluate(animation),
        alignment: _alignment?.evaluate(animation),
        decoration: _decoration?.evaluate(animation),
        foregroundDecoration: _foreground?.evaluate(animation));
  }
}
