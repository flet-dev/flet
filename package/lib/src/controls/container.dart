import 'dart:convert';
import 'dart:typed_data';

import 'package:collection/collection.dart';
import '../protocol/container_tap_event_data.dart';
import '../utils/animations.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/gradient.dart';
import '../utils/images.dart';
import '../utils/uri.dart';
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

    final ws = FletAppServices.of(context).ws;

    return StoreConnector<AppState, Uri?>(
        distinct: true,
        converter: (store) => store.state.pageUri,
        builder: (context, pageUri) {
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
            var uri = Uri.parse(imageSrc);
            image = DecorationImage(
                image: NetworkImage(uri.hasAuthority
                    ? imageSrc
                    : getAssetUri(pageUri!, imageSrc).toString()),
                repeat: imageRepeat,
                fit: imageFit,
                opacity: imageOpacity);
          }

          var gradient = parseGradient(Theme.of(context), control, "gradient");
          var blendMode = BlendMode.values.firstWhereOrNull((e) =>
              e.name.toLowerCase() ==
              control.attrString("blendMode", "")!.toLowerCase());

          var boxDecor = BoxDecoration(
              color: bgColor,
              gradient: gradient,
              image: image,
              backgroundBlendMode:
                  bgColor != null || gradient != null ? blendMode : null,
              border: parseBorder(Theme.of(context), control, "border"),
              borderRadius: parseBorderRadius(control, "borderRadius"));

          if ((onClick || onLongPress || onHover) && ink && !disabled) {
            var ink = Ink(
                child: InkWell(
                    onTap: onClick || onHover
                        ? () {
                            debugPrint("Container ${control.id} clicked!");
                            ws.pageEventFromWeb(
                                eventTarget: control.id,
                                eventName: "click",
                                eventData: control.attrs["data"] ?? "");
                          }
                        : null,
                    onLongPress: onLongPress || onHover
                        ? () {
                            debugPrint("Container ${control.id} long pressed!");
                            ws.pageEventFromWeb(
                                eventTarget: control.id,
                                eventName: "long_press",
                                eventData: control.attrs["data"] ?? "");
                          }
                        : null,
                    onHover: onHover
                        ? (value) {
                            debugPrint("Container ${control.id} hovered!");
                            ws.pageEventFromWeb(
                                eventTarget: control.id,
                                eventName: "hover",
                                eventData: value.toString());
                          }
                        : null,
                    child: Container(
                      child: child,
                      padding: parseEdgeInsets(control, "padding"),
                      alignment: parseAlignment(control, "alignment"),
                    ),
                    borderRadius: parseBorderRadius(control, "borderRadius")),
                decoration: boxDecor);
            return constrainedControl(
                animation == null
                    ? Container(
                        margin: parseEdgeInsets(control, "margin"),
                        child: ink,
                      )
                    : AnimatedContainer(
                        duration: animation.duration,
                        curve: animation.curve,
                        margin: parseEdgeInsets(control, "margin"),
                        child: ink),
                parent,
                control);
          } else {
            Widget container = animation == null
                ? Container(
                    width: control.attrDouble("width"),
                    height: control.attrDouble("height"),
                    padding: parseEdgeInsets(control, "padding"),
                    margin: parseEdgeInsets(control, "margin"),
                    alignment: parseAlignment(control, "alignment"),
                    decoration: boxDecor,
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
                    child: child);

            if ((onClick || onLongPress || onHover) && !disabled) {
              container = MouseRegion(
                cursor: SystemMouseCursors.click,
                onEnter: onHover
                    ? (value) {
                        debugPrint(
                            "Container's mouse region ${control.id} entered!");
                        ws.pageEventFromWeb(
                            eventTarget: control.id,
                            eventName: "hover",
                            eventData: "true");
                      }
                    : null,
                onExit: onHover
                    ? (value) {
                        debugPrint(
                            "Container's mouse region ${control.id} exited!");
                        ws.pageEventFromWeb(
                            eventTarget: control.id,
                            eventName: "hover",
                            eventData: "false");
                      }
                    : null,
                child: GestureDetector(
                  child: container,
                  onTapDown: onClick
                      ? (details) {
                          debugPrint("Container ${control.id} clicked!");
                          ws.pageEventFromWeb(
                              eventTarget: control.id,
                              eventName: "click",
                              eventData: json.encode(ContainerTapEventData(
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
                          ws.pageEventFromWeb(
                              eventTarget: control.id,
                              eventName: "long_press",
                              eventData: control.attrs["data"] ?? "");
                        }
                      : null,
                ),
              );
            }
            return constrainedControl(container, parent, control);
          }
        });
  }
}
