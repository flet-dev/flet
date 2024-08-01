import 'dart:convert';
import 'dart:io' as io;
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

import '../controls/error.dart';
import '../models/control.dart';
import '../models/page_args_model.dart';
import 'alignment.dart';
import 'borders.dart';
import 'collections.dart';
import 'colors.dart';
import 'gradient.dart';
import 'images.dart';
import 'numbers.dart';
import 'others.dart';
import 'transforms.dart';

List<BoxShadow> parseBoxShadow(
    ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName);
  if (v == null) {
    return [];
  }

  final j1 = json.decode(v);
  return boxShadowsFromJSON(theme, j1);
}

List<BoxShadow> boxShadowsFromJSON(ThemeData theme, dynamic json) {
  if (json == null) {
    return [];
  }
  if (json is List) {
    return json.map((e) => boxShadowFromJSON(theme, e)).toList();
  } else {
    return [boxShadowFromJSON(theme, json)];
  }
}

BoxShadow boxShadowFromJSON(ThemeData theme, dynamic json) {
  var offset = json["offset"] != null ? offsetFromJSON(json["offset"]) : null;
  return BoxShadow(
      color: parseColor(theme, json["color"], const Color(0xFF000000))!,
      offset: offset != null ? Offset(offset.x, offset.y) : Offset.zero,
      blurStyle: json["blur_style"] != null
          ? BlurStyle.values
              .firstWhere((e) => e.name.toLowerCase() == json["blur_style"])
          : BlurStyle.normal,
      blurRadius: parseDouble(json["blur_radius"], 0)!,
      spreadRadius: parseDouble(json["spread_radius"], 0)!);
}

BoxDecoration? parseBoxDecoration(ThemeData theme, Control control,
    String propName, PageArgsModel? pageArgs) {
  var v = control.attrString(propName);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return boxDecorationFromJSON(theme, j1, pageArgs);
}

BoxDecoration? boxDecorationFromJSON(
    ThemeData theme, dynamic json, PageArgsModel? pageArgs) {
  if (json == null) {
    return null;
  }
  return BoxDecoration(
    color: parseColor(theme, json["bgcolor"]),
    border: borderFromJSON(theme, json["border"]),
    shape: parseBoxShape(json["shape"], BoxShape.rectangle)!,
    borderRadius: borderRadiusFromJSON(json["border_radius"]),
    backgroundBlendMode: parseBlendMode(json["blend_mode"]),
    boxShadow: boxShadowsFromJSON(theme, json["box_shadow"]),
    gradient: gradientFromJSON(theme, json["gradient"]),
    image: decorationImageFromJSON(theme, json["image"], pageArgs),
  );
}

DecorationImage? parseDecorationImage(ThemeData theme, Control control,
    String propName, PageArgsModel? pageArgs) {
  var v = control.attrString(propName);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return decorationImageFromJSON(theme, j1, pageArgs);
}

DecorationImage? decorationImageFromJSON(
    ThemeData theme, dynamic json, PageArgsModel? pageArgs) {
  if (json == null) {
    return null;
  }
  var src = json["src"];
  var srcBase64 = json["src_base64"];
  ImageProvider? image = getImageProvider(src, srcBase64, pageArgs);
  if (image == null) {
    return null;
  }
  return DecorationImage(
    image: image,
    colorFilter: colorFilterFromJSON(json["color_filter"], theme),
    fit: parseBoxFit(json["fit"]),
    alignment: alignmentFromJson(json["alignment"], Alignment.center)!,
    repeat: parseImageRepeat(json["repeat"], ImageRepeat.noRepeat)!,
    matchTextDirection: parseBool(json["match_text_direction"], false)!,
    scale: parseDouble(json["scale"], 1.0)!,
    opacity: parseDouble(json["opacity"], 1.0)!,
    filterQuality:
        parseFilterQuality(json["filter_quality"], FilterQuality.low)!,
    invertColors: parseBool(json["invert_colors"], false)!,
    isAntiAlias: parseBool(json["anti_alias"], false)!,
  );
}

ImageProvider? getImageProvider(
    String? src, String? srcBase64, PageArgsModel? pageArgs) {
  if (srcBase64 != null && srcBase64 != "") {
    try {
      Uint8List bytes = base64Decode(srcBase64);
      return MemoryImage(bytes);
    } catch (ex) {
      debugPrint("Error decoding base64: ${ex.toString()}");
      return null;
    }
  } else if (src != null && src != "") {
    if (pageArgs == null) {
      return null;
    }
    var assetSrc = getAssetSrc(src, pageArgs.pageUri!, pageArgs.assetsDir);

    return assetSrc.isFile
        ? getFileImageProvider(assetSrc.path)
        : NetworkImage(assetSrc.path);
  } else {
    return null;
  }
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
  bool excludeFromSemantics = false,
  FilterQuality filterQuality = FilterQuality.low,
  bool disabled = false,
  required PageArgsModel pageArgs,
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
            colorBlendMode: colorBlendMode,
            gaplessPlayback: gaplessPlayback ?? true,
            semanticLabel: semanticsLabel);
      }
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
  return const ErrorControl("Either src or src_base64 must be specified.");
}
