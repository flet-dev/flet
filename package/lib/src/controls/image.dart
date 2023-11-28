import 'dart:convert';
import 'dart:io' as io;

import 'package:collection/collection.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:flutter_svg/svg.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/page_args_model.dart';
import '../utils/borders.dart';
import '../utils/collections.dart';
import '../utils/colors.dart';
import '../utils/images.dart';
import 'create_control.dart';
import 'error.dart';

class ImageControl extends StatelessWidget {
  final Control? parent;
  final List<Control> children;
  final Control control;
  final bool parentDisabled;

  static const String svgTag = " xmlns=\"http://www.w3.org/2000/svg\"";

  const ImageControl(
      {Key? key,
      required this.parent,
      required this.children,
      required this.control,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Image build: ${control.id}");

    var src = control.attrString("src", "")!;
    var srcBase64 = control.attrString("srcBase64", "")!;
    if (src == "" && srcBase64 == "") {
      return const ErrorControl(
          "Image must have either \"src\" or \"src_base64\" specified.");
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
    var gaplessPlayback = control.attrBool("gaplessPlayback");
    bool disabled = control.isDisabled || parentDisabled;
    var errorContentCtrls =
        children.where((c) => c.name == "error_content" && c.isVisible);

    return StoreConnector<AppState, PageArgsModel>(
        distinct: true,
        converter: (store) => PageArgsModel.fromStore(store),
        builder: (context, pageArgs) {
          Widget? image;

          if (srcBase64 != "") {
            try {
              Uint8List bytes = base64Decode(srcBase64);
              if (arrayIndexOf(
                      bytes, Uint8List.fromList(utf8.encode(svgTag))) !=
                  -1) {
                image = SvgPicture.memory(bytes,
                    width: width,
                    height: height,
                    fit: fit ?? BoxFit.contain,
                    colorFilter: color != null
                        ? ColorFilter.mode(
                            color, colorBlendMode ?? BlendMode.srcIn)
                        : null,
                    semanticsLabel: semanticsLabel);
              } else {
                image = Image.memory(bytes,
                    width: width,
                    height: height,
                    repeat: repeat,
                    fit: fit,
                    color: color,
                    colorBlendMode: colorBlendMode,
                    gaplessPlayback: gaplessPlayback ?? true,
                    semanticLabel: semanticsLabel);
              }
            } catch (ex) {
              return ErrorControl("Error decoding base64: ${ex.toString()}");
            }
          } else if (src.contains(svgTag)) {
            image = SvgPicture.memory(Uint8List.fromList(utf8.encode(src)),
                width: width,
                height: height,
                fit: fit ?? BoxFit.contain,
                colorFilter: color != null
                    ? ColorFilter.mode(color, colorBlendMode ?? BlendMode.srcIn)
                    : null,
                semanticsLabel: semanticsLabel);
          } else {
            var assetSrc =
                getAssetSrc(src, pageArgs.pageUri!, pageArgs.assetsDir);

            if (assetSrc.isFile) {
              // from File
              if (assetSrc.path.endsWith(".svg")) {
                image = getSvgPictureFromFile(
                    src: assetSrc.path,
                    width: width,
                    height: height,
                    fit: fit ?? BoxFit.contain,
                    color: color,
                    blendMode: colorBlendMode ?? BlendMode.srcIn,
                    semanticsLabel: semanticsLabel);
              } else {
                image = Image.file(
                  io.File(assetSrc.path),
                  width: width,
                  height: height,
                  repeat: repeat,
                  fit: fit,
                  color: color,
                  gaplessPlayback: gaplessPlayback ?? false,
                  colorBlendMode: colorBlendMode,
                  semanticLabel: semanticsLabel,
                  errorBuilder: errorContentCtrls.isNotEmpty
                      ? (context, error, stackTrace) {
                          return createControl(
                              control, errorContentCtrls.first.id, disabled);
                        }
                      : null,
                );
              }
            } else {
              // URL
              if (assetSrc.path.endsWith(".svg")) {
                image = SvgPicture.network(assetSrc.path,
                    width: width,
                    height: height,
                    fit: fit ?? BoxFit.contain,
                    colorFilter: color != null
                        ? ColorFilter.mode(
                            color, colorBlendMode ?? BlendMode.srcIn)
                        : null,
                    semanticsLabel: semanticsLabel);
              } else {
                image = Image.network(assetSrc.path,
                    width: width,
                    height: height,
                    repeat: repeat,
                    fit: fit,
                    color: color,
                    gaplessPlayback: gaplessPlayback ?? false,
                    colorBlendMode: colorBlendMode,
                    semanticLabel: semanticsLabel,
                    errorBuilder: errorContentCtrls.isNotEmpty
                        ? (context, error, stackTrace) {
                            return createControl(
                                control, errorContentCtrls.first.id, disabled);
                          }
                        : null);
              }
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
