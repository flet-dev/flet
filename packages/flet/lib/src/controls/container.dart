import 'package:flutter/material.dart';

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

    var bgColor = control.getColor("bgColor", context);
    var contentCtrl = control.child("content");
    bool ink = control.getBool("ink", false)!;
    bool onClick = control.getBool("onclick", false)!;
    bool onTapDown = control.getBool("onTapDown", false)!;
    String url = control.getString("url", "")!;
    String? urlTarget = control.getString("urlTarget");
    bool onLongPress = control.getBool("onLongPress", false)!;
    bool onHover = control.getBool("onHover", false)!;
    bool ignoreInteractions = control.getBool("ignoreInteractions", false)!;
    bool disabled = control.disabled || control.parent!.disabled;
    Widget? child = contentCtrl != null
        ? ControlWidget(
            control: contentCtrl,
          )
        : null;

    var animation = parseAnimation(control, "animate");
    var blur = parseBlur(control, "blur");
    var colorFilter =
        parseColorFilter(control, "colorFilter", Theme.of(context));
    var width = control.getDouble("width");
    var height = control.getDouble("height");
    var padding = parseEdgeInsets(control, "padding");
    var margin = parseEdgeInsets(control, "margin");
    var alignment = parseAlignment(control, "alignment");

    var borderRadius = parseBorderRadius(control, "borderRadius");
    var clipBehavior = parseClip(control.getString("clipBehavior"),
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
      blendMode: parseBlendMode(control.getString("blendMode")),
      image: decorationImage,
    );
    var boxForegroundDecoration =
        parseBoxDecoration(context, control, "foregroundDecoration");
    Widget? container;

    var onAnimationEnd = control.getBool("onAnimationEnd", false)!
        ? () {
            FletBackend.of(context)
                .triggerControlEvent(control, "animation_end", "container");
          }
        : null;
    if ((onClick || url != "" || onLongPress || onHover || onTapDown) &&
        ink &&
        !disabled) {
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
          !disabled) {
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
