import 'dart:convert';
import 'dart:typed_data';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/gradient.dart';
import '../utils/images.dart';
import '../utils/launch_url.dart';
import '../utils/shadows.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_control_stateless_mixin.dart';

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

class ContainerControl extends StatelessWidget with FletControlStatelessMixin {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const ContainerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  Widget build(BuildContext context) {
    debugPrint("Container build: ${control.id}");

    var bgColor = HexColor.fromString(
        Theme.of(context), control.attrString("bgColor", "")!);
    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool ink = control.attrBool("ink", false)!;
    bool onClick = control.attrBool("onclick", false)!;
    String url = control.attrString("url", "")!;
    String? urlTarget = control.attrString("urlTarget");
    bool onLongPress = control.attrBool("onLongPress", false)!;
    bool onHover = control.attrBool("onHover", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    var imageSrc = control.attrString("imageSrc", "")!;
    var imageSrcBase64 = control.attrString("imageSrcBase64", "")!;
    var imageRepeat = parseImageRepeat(control, "imageRepeat");
    var imageFit = parseBoxFit(control, "imageFit");
    var imageOpacity = control.attrDouble("imageOpacity", 1)!;

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled)
        : null;

    var animation = parseAnimation(control, "animate");
    var blur = parseBlur(control, "blur");

    return withPageArgs((context, pageArgs) {
      DecorationImage? image;

      if (imageSrcBase64 != "") {
        try {
          Uint8List bytes = base64Decode(imageSrcBase64);
          image = DecorationImage(
              image: MemoryImage(bytes),
              repeat: imageRepeat,
              fit: imageFit,
              opacity: imageOpacity);
        } catch (ex) {
          return ErrorControl("Error decoding base64: ${ex.toString()}");
        }
      } else if (imageSrc != "") {
        var assetSrc =
            getAssetSrc(imageSrc, pageArgs.pageUri!, pageArgs.assetsDir);

        image = DecorationImage(
            image: assetSrc.isFile
                ? getFileImageProvider(assetSrc.path)
                : NetworkImage(assetSrc.path),
            repeat: imageRepeat,
            fit: imageFit,
            opacity: imageOpacity);
      }

      var gradient = parseGradient(Theme.of(context), control, "gradient");
      var blendMode = BlendMode.values.firstWhereOrNull((e) =>
          e.name.toLowerCase() ==
          control.attrString("blendMode", "")!.toLowerCase());
      var shape = BoxShape.values.firstWhere(
          (e) =>
              e.name.toLowerCase() ==
              control.attrString("shape", "")!.toLowerCase(),
          orElse: () => BoxShape.rectangle);

      var borderRadius = parseBorderRadius(control, "borderRadius");

      var clipBehavior = Clip.values.firstWhere(
          (e) =>
              e.name.toLowerCase() ==
              control.attrString("clipBehavior", "")!.toLowerCase(),
          orElse: () => borderRadius != null ? Clip.antiAlias : Clip.none);

      var boxDecor = BoxDecoration(
          color: bgColor,
          gradient: gradient,
          image: image,
          backgroundBlendMode:
              bgColor != null || gradient != null ? blendMode : null,
          border: parseBorder(Theme.of(context), control, "border"),
          borderRadius: borderRadius,
          shape: shape,
          boxShadow: parseBoxShadow(Theme.of(context), control, "shadow"));

      Widget? result;

      if ((onClick || url != "" || onLongPress || onHover) &&
          ink &&
          !disabled) {
        var ink = Ink(
            decoration: boxDecor,
            child: InkWell(
              // Dummy callback to enable widget
              // see https://github.com/flutter/flutter/issues/50116#issuecomment-582047374
              // and https://github.com/flutter/flutter/blob/eed80afe2c641fb14b82a22279d2d78c19661787/packages/flutter/lib/src/material/ink_well.dart#L1125-L1129
              onTap: onHover ? () {} : null,
              onTapDown: onClick || url != ""
                  ? (details) {
                      debugPrint("Container ${control.id} clicked!");
                      if (url != "") {
                        openWebBrowser(url, webWindowName: urlTarget);
                      }
                      if (onClick) {
                        sendControlEvent(
                            context,
                            control.id,
                            "click",
                            json.encode(ContainerTapEvent(
                                    localX: details.localPosition.dx,
                                    localY: details.localPosition.dy,
                                    globalX: details.globalPosition.dx,
                                    globalY: details.globalPosition.dy)
                                .toJson()));
                      }
                    }
                  : null,
              onLongPress: onLongPress
                  ? () {
                      debugPrint("Container ${control.id} long pressed!");
                      sendControlEvent(context, control.id, "long_press", "");
                    }
                  : null,
              onHover: onHover
                  ? (value) {
                      debugPrint("Container ${control.id} hovered!");
                      sendControlEvent(
                          context, control.id, "hover", value.toString());
                    }
                  : null,
              borderRadius: borderRadius,
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
                clipBehavior: Clip.none,
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
                        sendControlEvent(
                            context, control.id, "animation_end", "container");
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
                decoration: boxDecor,
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
                decoration: boxDecor,
                clipBehavior: clipBehavior,
                onEnd: control.attrBool("onAnimationEnd", false)!
                    ? () {
                        sendControlEvent(
                            context, control.id, "animation_end", "container");
                      }
                    : null,
                child: child);

        if ((onClick || onLongPress || onHover || url != "") && !disabled) {
          result = MouseRegion(
            cursor: onClick || url != ""
                ? SystemMouseCursors.click
                : MouseCursor.defer,
            onEnter: onHover
                ? (value) {
                    debugPrint(
                        "Container's mouse region ${control.id} entered!");
                    sendControlEvent(context, control.id, "hover", "true");
                  }
                : null,
            onExit: onHover
                ? (value) {
                    debugPrint(
                        "Container's mouse region ${control.id} exited!");
                    sendControlEvent(context, control.id, "hover", "false");
                  }
                : null,
            child: GestureDetector(
              onTapDown: onClick || url != ""
                  ? (details) {
                      debugPrint("Container ${control.id} clicked!");
                      if (url != "") {
                        openWebBrowser(url, webWindowName: urlTarget);
                      }
                      if (onClick) {
                        sendControlEvent(
                            context,
                            control.id,
                            "click",
                            json.encode(ContainerTapEvent(
                                    localX: details.localPosition.dx,
                                    localY: details.localPosition.dy,
                                    globalX: details.globalPosition.dx,
                                    globalY: details.globalPosition.dy)
                                .toJson()));
                      }
                    }
                  : null,
              onLongPress: onLongPress
                  ? () {
                      debugPrint("Container ${control.id} clicked!");
                      sendControlEvent(context, control.id, "long_press", "");
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

      return constrainedControl(context, result, parent, control);
    });
  }
}
