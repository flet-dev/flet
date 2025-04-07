import 'dart:convert';
import 'dart:io' as io;
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../widgets/error.dart';
import 'alignment.dart';
import 'borders.dart';
import 'collections.dart';
import 'colors.dart';
import 'gradient.dart';
import 'images.dart';
import 'misc.dart';
import 'numbers.dart';
import 'transforms.dart';

BoxConstraints? parseBoxConstraints(dynamic value,
    [BoxConstraints? defaultValue]) {
  if (value == null) return defaultValue;

  return BoxConstraints(
    minHeight: parseDouble(value["min_height"], 0.0)!,
    minWidth: parseDouble(value["min_width"], 0.0)!,
    maxHeight: parseDouble(value["max_height"], double.infinity)!,
    maxWidth: parseDouble(value["max_width"], double.infinity)!,
  );
}

List<BoxShadow>? parseBoxShadows(dynamic value, ThemeData theme,
    [List<BoxShadow>? defaultValue]) {
  if (value == null) return defaultValue;
  if (value is List) {
    return value.map((e) => parseBoxShadow(e, theme)).toList();
  } else {
    return [parseBoxShadow(json, theme)];
  }
}

BoxShadow parseBoxShadow(dynamic value, ThemeData theme) {
  var offset = parseOffset(value["offset"]);
  return BoxShadow(
      color: parseColor(value["color"], theme, const Color(0xFF000000))!,
      offset: offset != null ? Offset(offset.dx, offset.dy) : Offset.zero,
      blurStyle: value["blur_style"] != null
          ? BlurStyle.values
              .firstWhere((e) => e.name.toLowerCase() == value["blur_style"])
          : BlurStyle.normal,
      blurRadius: parseDouble(value["blur_radius"], 0)!,
      spreadRadius: parseDouble(value["spread_radius"], 0)!);
}

BoxDecoration? parseBoxDecoration(dynamic value, BuildContext context,
    [BoxDecoration? defaultValue]) {
  if (value == null) return defaultValue;
  var theme = Theme.of(context);

  var shape = parseBoxShape(value["shape"], BoxShape.rectangle)!;
  var borderRadius = parseBorderRadius(value["border_radius"]);
  var color = parseColor(value["color"], theme);
  var gradient = parseGradient(value["gradient"], theme);
  var blendMode = parseBlendMode(value["blend_mode"]);

  return BoxDecoration(
    color: color,
    border: parseBorder(value["border"], theme),
    shape: shape,
    borderRadius: shape == BoxShape.circle ? null : borderRadius,
    backgroundBlendMode: color != null || gradient != null ? blendMode : null,
    boxShadow: parseBoxShadows(value["shadow"], theme),
    gradient: gradient,
    image: parseDecorationImage(value["image"], context),
  );
}

BoxDecoration? boxDecorationFromDetails({
  Color? color,
  Border? border,
  BoxShape? shape,
  BorderRadius? borderRadius,
  BlendMode? blendMode,
  List<BoxShadow>? boxShadow,
  Gradient? gradient,
  DecorationImage? image,
}) {
  bool hasCustomProperties = color != null ||
      border != null ||
      borderRadius != null ||
      gradient != null ||
      shape != null ||
      boxShadow != null ||
      image != null;

  // If no custom properties are provided, return null
  if (!hasCustomProperties) {
    return null;
  }

  return BoxDecoration(
    color: color,
    border: border,
    backgroundBlendMode: color != null || gradient != null ? blendMode : null,
    borderRadius: shape == BoxShape.circle ? null : borderRadius,
    gradient: gradient,
    shape: shape ?? BoxShape.rectangle,
    boxShadow: boxShadow,
    image: image,
  );
}

DecorationImage? parseDecorationImage(dynamic value, BuildContext context,
    [DecorationImage? defaultValue]) {
  if (value == null) return defaultValue;

  var src = value["src"];
  var srcBase64 = value["src_base64"];
  ImageProvider? image = getImageProvider(context, src, srcBase64);
  if (image == null) {
    return defaultValue;
  }
  return DecorationImage(
    image: image,
    colorFilter: parseColorFilter(value["color_filter"], Theme.of(context)),
    fit: parseBoxFit(value["fit"]),
    alignment: parseAlignment(value["alignment"], Alignment.center)!,
    repeat: parseImageRepeat(value["repeat"], ImageRepeat.noRepeat)!,
    matchTextDirection: parseBool(value["match_text_direction"], false)!,
    scale: parseDouble(value["scale"], 1.0)!,
    opacity: parseDouble(value["opacity"], 1.0)!,
    filterQuality:
        parseFilterQuality(value["filter_quality"], FilterQuality.medium)!,
    invertColors: parseBool(value["invert_colors"], false)!,
    isAntiAlias: parseBool(value["anti_alias"], false)!,
  );
}

ImageProvider? getImageProvider(
    BuildContext context, String? src, String? srcBase64) {
  src = src?.trim();
  srcBase64 = srcBase64?.trim();

  if (srcBase64 != null && srcBase64 != "") {
    try {
      Uint8List bytes = base64Decode(srcBase64);
      return MemoryImage(bytes);
    } catch (ex) {
      debugPrint("getImageProvider failed decoding srcBase64");
    }
  }
  if (src != null && src != "") {
    var assetSrc = FletBackend.of(context).getAssetSource(src);

    return assetSrc.isFile
        ? getFileImageProvider(assetSrc.path)
        : NetworkImage(assetSrc.path);
  }
  return null;
}

Widget buildImage({
  required BuildContext context,
  required Control control,
  required Widget? errorCtrl,
  required String? src,
  required String? srcBase64,
  double? width,
  double? height,
  ImageRepeat repeat = ImageRepeat.noRepeat,
  BoxFit? fit,
  BlendMode? colorBlendMode,
  Color? color,
  String? semanticsLabel,
  bool? gaplessPlayback,
  int? cacheWidth,
  int? cacheHeight,
  bool antiAlias = false,
  bool excludeFromSemantics = false,
  FilterQuality filterQuality = FilterQuality.low,
  bool disabled = false,
}) {
  Widget? image;
  const String svgTag = " xmlns=\"http://www.w3.org/2000/svg\"";

  if (srcBase64 != null && srcBase64.isNotEmpty) {
    try {
      Uint8List bytes = base64Decode(srcBase64);
      if (arrayIndexOf(bytes, Uint8List.fromList(utf8.encode(svgTag))) != -1) {
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
            cacheHeight: cacheHeight,
            cacheWidth: cacheWidth,
            filterQuality: filterQuality,
            isAntiAlias: antiAlias,
            colorBlendMode: colorBlendMode,
            gaplessPlayback: gaplessPlayback ?? true,
            semanticLabel: semanticsLabel);
      }
      return image;
    } catch (ex) {
      return ErrorControl("Error decoding base64: ${ex.toString()}");
    }
  } else if (src != null && src.isNotEmpty) {
    if (src.contains(svgTag)) {
      image = SvgPicture.memory(Uint8List.fromList(utf8.encode(src)),
          width: width,
          height: height,
          fit: fit ?? BoxFit.contain,
          colorFilter: color != null
              ? ColorFilter.mode(color, colorBlendMode ?? BlendMode.srcIn)
              : null,
          semanticsLabel: semanticsLabel);
    } else {
      var assetSrc = FletBackend.of(context).getAssetSource(src);

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
            isAntiAlias: antiAlias,
            cacheHeight: cacheHeight,
            cacheWidth: cacheWidth,
            gaplessPlayback: gaplessPlayback ?? false,
            colorBlendMode: colorBlendMode,
            semanticLabel: semanticsLabel,
            errorBuilder: errorCtrl != null
                ? (context, error, stackTrace) {
                    return errorCtrl;
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
              cacheHeight: cacheHeight,
              cacheWidth: cacheWidth,
              isAntiAlias: antiAlias,
              excludeFromSemantics: excludeFromSemantics,
              fit: fit,
              color: color,
              gaplessPlayback: gaplessPlayback ?? false,
              colorBlendMode: colorBlendMode,
              semanticLabel: semanticsLabel,
              errorBuilder: errorCtrl != null
                  ? (context, error, stackTrace) {
                      return errorCtrl;
                    }
                  : null);
        }
      }
    }
    return image;
  }
  return const ErrorControl("A valid src or src_base64 must be specified.");
}

extension BoxParsers on Control {
  BoxConstraints? getBoxConstraints(String propertyName,
      [BoxConstraints? defaultValue]) {
    return parseBoxConstraints(get(propertyName), defaultValue);
  }

  List<BoxShadow>? getBoxShadows(String propertyName, ThemeData theme,
      [List<BoxShadow>? defaultValue]) {
    return parseBoxShadows(get(propertyName), theme, defaultValue);
  }

  BoxDecoration? getBoxDecoration(String propertyName, BuildContext context,
      [BoxDecoration? defaultValue]) {
    return parseBoxDecoration(get(propertyName), context, defaultValue);
  }

  DecorationImage? getDecorationImage(String propertyName, BuildContext context,
      [DecorationImage? defaultValue]) {
    return parseDecorationImage(get(propertyName), context, defaultValue);
  }
}