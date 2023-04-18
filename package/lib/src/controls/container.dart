import 'dart:convert';
import 'dart:typed_data';

import 'package:collection/collection.dart';
import 'package:flet/src/utils/shadows.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/page_args_model.dart';
import '../protocol/container_tap_event.dart';
import '../utils/alignment.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/gradient.dart';
import '../utils/images.dart';
import 'create_control.dart';
import 'error.dart';

class ContainerControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const ContainerControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Container build: ${control.id}");

    var bgColor = HexColor.fromString(
        Theme.of(context), control.attrString("bgColor", "")!);
    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool ink = control.attrBool("ink", false)!;
    bool onClick = control.attrBool("onclick", false)!;
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

    final server = FletAppServices.of(context).server;

    return StoreConnector<AppState, PageArgsModel>(
        distinct: true,
        converter: (store) => PageArgsModel.fromStore(store),
        builder: (context, pageArgs) {
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
              orElse: () =>
                  borderRadius != null ? Clip.antiAlias : Clip.hardEdge);

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

          if ((onClick || onLongPress || onHover) && ink && !disabled) {
            var ink = Ink(
                decoration: boxDecor,
                child: InkWell(
                  // Dummy callback to enable widget
                  // see https://github.com/flutter/flutter/issues/50116#issuecomment-582047374
                  // and https://github.com/flutter/flutter/blob/eed80afe2c641fb14b82a22279d2d78c19661787/packages/flutter/lib/src/material/ink_well.dart#L1125-L1129
                  onTap: onHover ? () {} : null,
                  onTapDown: onClick
                      ? (details) {
                          debugPrint("Container ${control.id} clicked!");
                          server.sendPageEvent(
                              eventTarget: control.id,
                              eventName: "click",
                              eventData: json.encode(ContainerTapEvent(
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
                          server.sendPageEvent(
                              eventTarget: control.id,
                              eventName: "long_press",
                              eventData: "");
                        }
                      : null,
                  onHover: onHover
                      ? (value) {
                          debugPrint("Container ${control.id} hovered!");
                          server.sendPageEvent(
                              eventTarget: control.id,
                              eventName: "hover",
                              eventData: value.toString());
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
                            server.sendPageEvent(
                                eventTarget: control.id,
                                eventName: "animation_end",
                                eventData: "container");
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
                            server.sendPageEvent(
                                eventTarget: control.id,
                                eventName: "animation_end",
                                eventData: "container");
                          }
                        : null,
                    child: child);

            if ((onClick || onLongPress || onHover) && !disabled) {
              result = MouseRegion(
                cursor: SystemMouseCursors.click,
                onEnter: onHover
                    ? (value) {
                        debugPrint(
                            "Container's mouse region ${control.id} entered!");
                        server.sendPageEvent(
                            eventTarget: control.id,
                            eventName: "hover",
                            eventData: "true");
                      }
                    : null,
                onExit: onHover
                    ? (value) {
                        debugPrint(
                            "Container's mouse region ${control.id} exited!");
                        server.sendPageEvent(
                            eventTarget: control.id,
                            eventName: "hover",
                            eventData: "false");
                      }
                    : null,
                child: GestureDetector(
                  onTapDown: onClick
                      ? (details) {
                          debugPrint("Container ${control.id} clicked!");
                          server.sendPageEvent(
                              eventTarget: control.id,
                              eventName: "click",
                              eventData: json.encode(ContainerTapEvent(
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
                          server.sendPageEvent(
                              eventTarget: control.id,
                              eventName: "long_press",
                              eventData: "");
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
