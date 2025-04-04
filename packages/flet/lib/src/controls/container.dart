import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/edge_insets.dart';
import '../utils/gradient.dart';
import '../utils/images.dart';
import '../utils/launch_url.dart';
import '../utils/others.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';
import 'control_widget.dart';

class ContainerTapEvent {
  final double localX;
  final double localY;
  final double globalX;
  final double globalY;

  ContainerTapEvent(
      {required this.localX,
      required this.localY,
      required this.globalX,
      required this.globalY});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'lx': localX,
        'ly': localY,
        'gx': globalX,
        'gy': globalY
      };
}

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
    var contentCtrl = control.child("content");
    bool ink = control.getBool("ink", false)!;
    bool onClick = control.getBool("on_click", false)!;
    bool onTapDown = control.getBool("on_tap_down", false)!;
    String url = control.getString("url", "")!;
    String? urlTarget = control.getString("url_target");
    bool onLongPress = control.getBool("on_long_press", false)!;
    bool onHover = control.getBool("on_hover", false)!;
    bool ignoreInteractions = control.getBool("ignore_interactions", false)!;
    Widget? child = contentCtrl != null
        ? ControlWidget(
            control: contentCtrl,
          )
        : null;

    var animation = parseAnimation(control, "animate");
    var blur = parseBlur(control, "blur");
    var colorFilter =
        parseColorFilter(control, "color_filter", Theme.of(context));
    var width = control.getDouble("width");
    var height = control.getDouble("height");
    var padding = parseEdgeInsets(control, "padding");
    var margin = parseEdgeInsets(control, "margin");
    var alignment = parseAlignment(control, "alignment");

    var borderRadius = parseBorderRadius(control, "border_radius");
    var clipBehavior = parseClip(control.getString("clip_behavior"),
        borderRadius != null ? Clip.antiAlias : Clip.none)!;
    var decorationImage = parseDecorationImage(context, control, "image");
    var boxDecoration = boxDecorationFromDetails(
      shape: parseBoxShape(control.getString("shape"), BoxShape.rectangle)!,
      color: bgColor,
      gradient: parseGradient(Theme.of(context), control, "gradient"),
      borderRadius: borderRadius,
      border: parseBorder(Theme.of(context), control, "border",
          Theme.of(context).colorScheme.primary),
      boxShadow: parseBoxShadow(Theme.of(context), control, "shadow"),
      blendMode: parseBlendMode(control.getString("blend_mode")),
      image: decorationImage,
    );
    var boxForegroundDecoration =
        parseBoxDecoration(context, control, "foreground_decoration");
    Widget? container;

    var onAnimationEnd = control.getBool("on_animation_end", false)!
        ? () {
            FletBackend.of(context)
                .triggerControlEvent(control, "animation_end", "container");
          }
        : null;
    if ((onClick || url != "" || onLongPress || onHover || onTapDown) &&
        ink &&
        !control.disabled) {
      var ink = Material(
          color: Colors.transparent,
          borderRadius: boxDecoration!.borderRadius,
          child: InkWell(
            // Dummy callback to enable widget
            // see https://github.com/flutter/flutter/issues/50116#issuecomment-582047374
            // and https://github.com/flutter/flutter/blob/eed80afe2c641fb14b82a22279d2d78c19661787/packages/flutter/lib/src/material/ink_well.dart#L1125-L1129
            onTap: onClick || url != "" || onTapDown
                ? () {
                    debugPrint("Container ${control.id} clicked!");
                    if (url != "") {
                      openWebBrowser(url, webWindowName: urlTarget);
                    }
                    if (onClick) {
                      FletBackend.of(context)
                          .triggerControlEvent(control, "click");
                    }
                  }
                : null,
            onTapDown: onTapDown
                ? (details) {
                    FletBackend.of(context).triggerControlEvent(
                        control,
                        "tap_down",
                        ContainerTapEvent(
                                localX: details.localPosition.dx,
                                localY: details.localPosition.dy,
                                globalX: details.globalPosition.dx,
                                globalY: details.globalPosition.dy)
                            .toJson());
                  }
                : null,
            onLongPress: onLongPress
                ? () {
                    debugPrint("Container ${control.id} long pressed!");
                    FletBackend.of(context)
                        .triggerControlEvent(control, "long_press");
                  }
                : null,
            onHover: onHover
                ? (value) {
                    debugPrint("Container ${control.id} hovered!");
                    FletBackend.of(context)
                        .triggerControlEvent(control, "hover", value);
                  }
                : null,
            borderRadius: borderRadius,
            splashColor: control.getColor("inkColor", context),
            child: Container(
              padding: padding,
              alignment: alignment,
              clipBehavior: Clip.none,
              child: child,
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
              child: child)
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
              child: child);

      if ((onClick || onLongPress || onHover || onTapDown || url != "") &&
          !control.disabled) {
        container = MouseRegion(
          cursor: onClick || onTapDown || url != ""
              ? SystemMouseCursors.click
              : MouseCursor.defer,
          onEnter: onHover
              ? (value) {
                  debugPrint("Container's mouse region ${control.id} entered!");
                  FletBackend.of(context)
                      .triggerControlEvent(control, "hover", true);
                }
              : null,
          onExit: onHover
              ? (value) {
                  debugPrint("Container's mouse region ${control.id} exited!");
                  FletBackend.of(context)
                      .triggerControlEvent(control, "hover", false);
                }
              : null,
          child: GestureDetector(
            onTap: onClick || url != ""
                ? () {
                    debugPrint("Container ${control.id} clicked!");
                    if (url != "") {
                      openWebBrowser(url, webWindowName: urlTarget);
                    }
                    if (onClick) {
                      FletBackend.of(context)
                          .triggerControlEvent(control, "click");
                    }
                  }
                : null,
            onTapDown: onTapDown
                ? (details) {
                    FletBackend.of(context).triggerControlEvent(
                        control,
                        "tap_down",
                        ContainerTapEvent(
                                localX: details.localPosition.dx,
                                localY: details.localPosition.dy,
                                globalX: details.globalPosition.dx,
                                globalY: details.globalPosition.dy)
                            .toJson());
                  }
                : null,
            onLongPress: onLongPress
                ? () {
                    debugPrint("Container ${control.id} clicked!");
                    FletBackend.of(context)
                        .triggerControlEvent(control, "long_press");
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

    return ConstrainedControl(
      control: control,
      child: container,
    );
  }
}
