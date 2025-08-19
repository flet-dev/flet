import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

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
    var onClick = control.getBool("on_click", false)!;
    var onTapDown = control.getBool("on_tap_down", false)!;
    var url = control.getUrl("url");
    var onLongPress = control.getBool("on_long_press", false)!;
    var onHover = control.getBool("on_hover", false)!;
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
      gradient: parseGradient(control.get("gradient"), Theme.of(context)),
      borderRadius: borderRadius,
      border: control.getBorder("border", Theme.of(context),
          defaultSideColor: Theme.of(context).colorScheme.primary),
      boxShadow: control.getBoxShadows("shadow", Theme.of(context)),
      blendMode: control.getBlendMode("blend_mode"),
      image: decorationImage,
    );
    var boxForegroundDecoration =
        parseBoxDecoration(control.get("foreground_decoration"), context);
    Widget? container;

    var onAnimationEnd = control.getBool("on_animation_end", false)!
        ? () => control.triggerEvent("animation_end" "container")
        : null;
    if ((onClick || url != null || onLongPress || onHover || onTapDown) &&
        ink &&
        !control.disabled) {
      var ink = Material(
          color: Colors.transparent,
          borderRadius: boxDecoration!.borderRadius,
          child: InkWell(
            // Dummy callback to enable widget
            // see https://github.com/flutter/flutter/issues/50116#issuecomment-582047374
            // and https://github.com/flutter/flutter/blob/eed80afe2c641fb14b82a22279d2d78c19661787/packages/flutter/lib/src/material/ink_well.dart#L1125-L1129
            onTap: onClick || url != null || onTapDown
                ? () {
                    if (url != null) {
                      openWebBrowser(url);
                    }
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
            child: Container(
              padding: padding,
              alignment: alignment,
              clipBehavior: Clip.none,
              child: content,
            ),
          ));

      container = animation == null
          ? Container(
              width: width,
              height: height,
              margin: margin,
              clipBehavior: clipBehavior,
              decoration: boxDecoration,
              foregroundDecoration: boxForegroundDecoration,
              child: ink,
            )
          : AnimatedContainer(
              duration: animation.duration,
              curve: animation.curve,
              width: width,
              height: height,
              margin: margin,
              alignment: alignment,
              padding: padding,
              decoration: boxDecoration,
              foregroundDecoration: boxForegroundDecoration,
              clipBehavior: clipBehavior,
              onEnd: onAnimationEnd,
              child: ink);
    } else {
      container = animation == null
          ? Container(
              width: width,
              height: height,
              margin: margin,
              padding: padding,
              alignment: alignment,
              decoration: boxDecoration,
              foregroundDecoration: boxForegroundDecoration,
              clipBehavior: clipBehavior,
              child: content)
          : AnimatedContainer(
              duration: animation.duration,
              curve: animation.curve,
              width: width,
              height: height,
              margin: margin,
              padding: padding,
              alignment: alignment,
              decoration: boxDecoration,
              foregroundDecoration: boxForegroundDecoration,
              clipBehavior: clipBehavior,
              onEnd: onAnimationEnd,
              child: content);

      if ((onClick || onLongPress || onHover || onTapDown || url != null) &&
          !control.disabled) {
        container = MouseRegion(
          cursor: onClick || onTapDown || url != null
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
            onTap: onClick || url != null
                ? () {
                    if (url != null) {
                      openWebBrowser(url);
                    }
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

    if (ignoreInteractions) {
      container = IgnorePointer(child: container);
    }

    return ConstrainedControl(control: control, child: container);
  }
}
