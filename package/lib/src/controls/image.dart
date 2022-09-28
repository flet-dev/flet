import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:flutter_svg/svg.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/collections.dart';
import '../utils/colors.dart';
import '../utils/images.dart';
import '../utils/uri.dart';
import 'create_control.dart';
import 'error.dart';

class ImageControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  static const String SVG_TAG = "<svg";

  const ImageControl({Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Image build: ${control.id}");

    var src = control.attrString("src", "")!;
    var srcBase64 = control.attrString("srcBase64", "")!;
    if (src == "" && srcBase64 == "") {
      return const ErrorControl(
          "Image must have 'src' or 'src_base64' specified.");
    }
    double? width = control.attrDouble("width", null);
    double? height = control.attrDouble("height", null);
    var repeat = parseImageRepeat(control, "repeat");
    var fit = parseBoxFit(control, "fit");
    var colorBlendMode = BlendMode.values.firstWhereOrNull((e) =>
        e.name.toLowerCase() ==
        control.attrString("colorBlendMode", "")!.toLowerCase());
    var color = HexColor.fromString(
        Theme.of(context), control.attrString("color", "")!);
    String? semanticsLabel = control.attrString("semanticsLabel");
    var gaplessPlayback = control.attrBool("gaplessPlayback", false)!;

    return StoreConnector<AppState, Uri?>(
        distinct: true,
        converter: (store) => store.state.pageUri,
        builder: (context, pageUri) {
          Widget? image;

          if (srcBase64 != "") {
            try {
              Uint8List bytes = base64Decode(srcBase64);
              if (arrayIndexOf(
                      bytes, Uint8List.fromList(utf8.encode(SVG_TAG))) !=
                  -1) {
                image = SvgPicture.memory(bytes,
                    width: width,
                    height: height,
                    fit: fit ?? BoxFit.contain,
                    color: color,
                    colorBlendMode: colorBlendMode ?? BlendMode.srcIn,
                    semanticsLabel: semanticsLabel);
              } else {
                image = Image.memory(bytes,
                    width: width,
                    height: height,
                    repeat: repeat,
                    fit: fit,
                    color: color,
                    colorBlendMode: colorBlendMode,
                    gaplessPlayback: gaplessPlayback,
                    semanticLabel: semanticsLabel);
              }
            } catch (ex) {
              return ErrorControl("Error decoding base64: ${ex.toString()}");
            }
          } else if (src.contains(SVG_TAG)) {
            image = SvgPicture.memory(Uint8List.fromList(utf8.encode(src)),
                width: width,
                height: height,
                fit: fit ?? BoxFit.contain,
                color: color,
                colorBlendMode: colorBlendMode ?? BlendMode.srcIn,
                semanticsLabel: semanticsLabel);
          } else {
            var uri = Uri.parse(src);
            var imgSrc =
                uri.hasAuthority ? src : getAssetUri(pageUri!, src).toString();
            if (imgSrc.endsWith(".svg")) {
              image = SvgPicture.network(imgSrc,
                  width: width,
                  height: height,
                  fit: fit ?? BoxFit.contain,
                  color: color,
                  colorBlendMode: colorBlendMode ?? BlendMode.srcIn,
                  semanticsLabel: semanticsLabel);
            } else {
              image = Image.network(imgSrc,
                  width: width,
                  height: height,
                  repeat: repeat,
                  fit: fit,
                  color: color,
                  gaplessPlayback: gaplessPlayback,
                  colorBlendMode: colorBlendMode,
                  semanticLabel: semanticsLabel);
            }
          }

          return constrainedControl(
              context, _clipCorners(image, control), parent, control);
        });
  }

  Widget _clipCorners(Widget image, Control control) {
    var borderRadius = parseBorderRadius(control, "borderRadius");
    return borderRadius != null
        ? ClipRRect(
            borderRadius: borderRadius,
            child: image,
          )
        : image;
  }
}
