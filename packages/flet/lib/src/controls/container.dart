import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
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
import 'create_control.dart';
import 'flet_store_mixin.dart';

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
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const ContainerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("Container build: ${control.id}");

    var bgColor = control.attrColor("bgColor", context);
    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool ink = control.attrBool("ink", false)!;
    bool onClick = control.attrBool("onclick", false)!;
    bool onTapDown = control.attrBool("onTapDown", false)!;
    String url = control.attrString("url", "")!;
    String? urlTarget = control.attrString("urlTarget");
    bool onLongPress = control.attrBool("onLongPress", false)!;
    bool onHover = control.attrBool("onHover", false)!;
    bool disabled = control.isDisabled || parentDisabled;
    bool? adaptive = control.attrBool("adaptive") ?? parentAdaptive;

    var imageSrc = control.attrString("imageSrc", "")!;
    var imageSrcBase64 = control.attrString("imageSrcBase64", "")!;
    var imageRepeat = parseImageRepeat(
        control.attrString("imageRepeat"), ImageRepeat.noRepeat)!;
    var imageFit = parseBoxFit(control.attrString("imageFit"));
    var imageOpacity = control.attrDouble("imageOpacity", 1)!;

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled,
            parentAdaptive: adaptive)
        : null;

    var animation = parseAnimation(control, "animate");
    var blur = parseBlur(control, "blur");
    var colorFilter =
        parseColorFilter(control, "colorFilter", Theme.of(context));

    return withPageArgs((context, pageArgs) {
      ImageProvider? image =
          getImageProvider(imageSrc, imageSrcBase64, pageArgs);

      var gradient = parseGradient(Theme.of(context), control, "gradient");
      var blendMode = parseBlendMode(control.attrString("blendMode"));
      var shape =
          parseBoxShape(control.attrString("shape"), BoxShape.rectangle)!;

      var borderRadius = parseBorderRadius(control, "borderRadius");

      var clipBehavior = parseClip(control.attrString("clipBehavior"),
          borderRadius != null ? Clip.antiAlias : Clip.none)!;

      var decorationImage =
          parseDecorationImage(Theme.of(context), control, "image", pageArgs);

      var boxDecoration = parseBoxDecoration(
              Theme.of(context), control, "decoration", pageArgs) ??
          BoxDecoration(
              color: bgColor,
              gradient: gradient,
              image: decorationImage == null && image != null
                  ? DecorationImage(
                      image: image,
                      repeat: imageRepeat,
                      fit: imageFit,
                      opacity: imageOpacity)
                  : decorationImage,
              backgroundBlendMode:
                  bgColor != null || gradient != null ? blendMode : null,
              border: parseBorder(Theme.of(context), control, "border",
                  Theme.of(context).colorScheme.primary),
              borderRadius: borderRadius,
              shape: shape,
              boxShadow: parseBoxShadow(Theme.of(context), control, "shadow"));
      var boxForegroundDecoration = parseBoxDecoration(
          Theme.of(context), control, "foregroundDecoration", pageArgs);
      Widget? result;

      if ((onClick || url != "" || onLongPress || onHover || onTapDown) &&
          ink &&
          !disabled) {
        var ink = Material(
            color: Colors.transparent,
            borderRadius: boxDecoration.borderRadius,
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
                        backend.triggerControlEvent(control.id, "click");
                      }
                    }
                  : null,
              onTapDown: onTapDown
                  ? (details) {
                      backend.triggerControlEvent(
                          control.id,
                          "tap_down",
                          json.encode(ContainerTapEvent(
                                  localX: details.localPosition.dx,
                                  localY: details.localPosition.dy,
                                  globalX: details.globalPosition.dx,
                                  globalY: details.globalPosition.dy)
                              .toJson()));
                    }
                  : null,
              onLongPress: onLongPress
                  ? () {
                      debugPrint("Container ${control.id} long pressed!");
                      backend.triggerControlEvent(control.id, "long_press");
                    }
                  : null,
              onHover: onHover
                  ? (value) {
                      debugPrint("Container ${control.id} hovered!");
                      backend.triggerControlEvent(
                          control.id, "hover", value.toString());
                    }
                  : null,
              borderRadius: borderRadius,
              splashColor: control.attrColor("inkColor", context),
              child: Container(
                padding: parseEdgeInsets(control, "padding"),
                alignment: parseAlignment(control, "alignment"),
                clipBehavior: Clip.none,
                child: child,
              ),
            ));

        result = animation == null
            ? Container(
                width: control.attrDouble("width"),
                height: control.attrDouble("height"),
                margin: parseEdgeInsets(control, "margin"),
                clipBehavior: clipBehavior,
                decoration: boxDecoration,
                foregroundDecoration: boxForegroundDecoration,
                child: ink,
              )
            : AnimatedContainer(
                duration: animation.duration,
                curve: animation.curve,
                width: control.attrDouble("width"),
                height: control.attrDouble("height"),
                margin: parseEdgeInsets(control, "margin"),
                clipBehavior: clipBehavior,
                onEnd: control.attrBool("onAnimationEnd", false)!
                    ? () {
                        backend.triggerControlEvent(
                            control.id, "animation_end", "container");
                      }
                    : null,
                child: ink);
      } else {
        result = animation == null
            ? Container(
                width: control.attrDouble("width"),
                height: control.attrDouble("height"),
                padding: parseEdgeInsets(control, "padding"),
                margin: parseEdgeInsets(control, "margin"),
                alignment: parseAlignment(control, "alignment"),
                decoration: boxDecoration,
                foregroundDecoration: boxForegroundDecoration,
                clipBehavior: clipBehavior,
                child: child)
            : AnimatedContainer(
                duration: animation.duration,
                curve: animation.curve,
                width: control.attrDouble("width"),
                height: control.attrDouble("height"),
                padding: parseEdgeInsets(control, "padding"),
                margin: parseEdgeInsets(control, "margin"),
                alignment: parseAlignment(control, "alignment"),
                decoration: boxDecoration,
                foregroundDecoration: boxForegroundDecoration,
                clipBehavior: clipBehavior,
                onEnd: control.attrBool("onAnimationEnd", false)!
                    ? () {
                        backend.triggerControlEvent(
                            control.id, "animation_end", "container");
                      }
                    : null,
                child: child);

        if ((onClick || onLongPress || onHover || onTapDown || url != "") &&
            !disabled) {
          result = MouseRegion(
            cursor: onClick || onTapDown || url != ""
                ? SystemMouseCursors.click
                : MouseCursor.defer,
            onEnter: onHover
                ? (value) {
                    debugPrint(
                        "Container's mouse region ${control.id} entered!");
                    backend.triggerControlEvent(control.id, "hover", "true");
                  }
                : null,
            onExit: onHover
                ? (value) {
                    debugPrint(
                        "Container's mouse region ${control.id} exited!");
                    backend.triggerControlEvent(control.id, "hover", "false");
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
                        backend.triggerControlEvent(control.id, "click");
                      }
                    }
                  : null,
              onTapDown: onTapDown
                  ? (details) {
                      backend.triggerControlEvent(
                          control.id,
                          "tap_down",
                          json.encode(ContainerTapEvent(
                                  localX: details.localPosition.dx,
                                  localY: details.localPosition.dy,
                                  globalX: details.globalPosition.dx,
                                  globalY: details.globalPosition.dy)
                              .toJson()));
                    }
                  : null,
              onLongPress: onLongPress
                  ? () {
                      debugPrint("Container ${control.id} clicked!");
                      backend.triggerControlEvent(control.id, "long_press");
                    }
                  : null,
              child: result,
            ),
          );
        }
      }

      if (blur != null) {
        result = borderRadius != null
            ? ClipRRect(
                borderRadius: borderRadius,
                child: BackdropFilter(filter: blur, child: result))
            : ClipRect(child: BackdropFilter(filter: blur, child: result));
      }
      if (colorFilter != null) {
        result = ColorFiltered(colorFilter: colorFilter, child: result);
      }

      return constrainedControl(context, result, parent, control);
    });
  }
}
