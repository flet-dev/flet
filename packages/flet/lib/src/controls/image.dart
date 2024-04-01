import 'dart:convert';
import 'dart:io' as io;

import 'package:collection/collection.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/collections.dart';
import '../utils/images.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_store_mixin.dart';

class ImageControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final List<Control> children;
  final Control control;
  final bool parentDisabled;
  final FletControlBackend backend;

  static const String svgTag = " xmlns=\"http://www.w3.org/2000/svg\"";

  const ImageControl(
      {super.key,
      required this.parent,
      required this.children,
      required this.control,
      required this.parentDisabled,
      required this.backend});

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
    var color = control.attrColor("color", context);
    String? semanticsLabel = control.attrString("semanticsLabel");
    var gaplessPlayback = control.attrBool("gaplessPlayback");
    var excludeFromSemantics = control.attrBool("excludeFromSemantics", false)!;
    FilterQuality filterQuality = FilterQuality.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("filterQuality", "")!.toLowerCase(),
        orElse: () => FilterQuality.low);
    bool disabled = control.isDisabled || parentDisabled;
    var errorContentCtrls =
        children.where((c) => c.name == "error_content" && c.isVisible);

    return withPageArgs((context, pageArgs) {
      Widget? image;

      if (srcBase64 != "") {
        try {
          Uint8List bytes = base64Decode(srcBase64);
          if (arrayIndexOf(bytes, Uint8List.fromList(utf8.encode(svgTag))) !=
              -1) {
            image = SvgPicture.memory(bytes,
                width: width,
                height: height,
                fit: fit ?? BoxFit.contain,
                colorFilter: color != null
                    ? ColorFilter.mode(color, colorBlendMode ?? BlendMode.srcIn)
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
        var assetSrc = getAssetSrc(src, pageArgs.pageUri!, pageArgs.assetsDir);

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
              filterQuality: filterQuality,
              excludeFromSemantics: excludeFromSemantics,
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
                excludeFromSemantics: excludeFromSemantics,
                fit: fit ?? BoxFit.contain,
                colorFilter: color != null
                    ? ColorFilter.mode(color, colorBlendMode ?? BlendMode.srcIn)
                    : null,
                semanticsLabel: semanticsLabel);
          } else {
            image = Image.network(assetSrc.path,
                width: width,
                height: height,
                repeat: repeat,
                filterQuality: filterQuality,
                excludeFromSemantics: excludeFromSemantics,
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
