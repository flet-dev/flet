import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';

import '../models/control.dart';
import '../models/page_args_model.dart';
import 'alignment.dart';
import 'borders.dart';
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
  debugPrint("BOX DECORATION: $j1");
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