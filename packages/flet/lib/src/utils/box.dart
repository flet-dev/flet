import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

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
    return value.map((e) => parseBoxShadow(e, theme)!).toList();
  } else {
    return [parseBoxShadow(value, theme)!];
  }
}

BoxShadow? parseBoxShadow(dynamic value, ThemeData theme,
    [BoxShadow? defaultValue]) {
  if (value == null) return defaultValue;

  return BoxShadow(
      color: parseColor(value["color"], theme, Colors.black)!,
      offset: parseOffset(value["offset"], Offset.zero)!,
      blurStyle: parseBlurStyle(value["blur_style"], BlurStyle.normal)!,
      blurRadius: parseDouble(value["blur_radius"], 0)!,
      spreadRadius: parseDouble(value["spread_radius"], 0)!);
}

BoxDecoration? parseBoxDecoration(dynamic value, BuildContext context,
    [BoxDecoration? defaultValue]) {
  if (value == null) return defaultValue;
  var theme = Theme.of(context);

  var shape = parseBoxShape(value["shape"], BoxShape.rectangle)!;
  var borderRadius = parseBorderRadius(value["border_radius"]);
  var color = parseColor(value["bgcolor"], theme);
  var gradient = parseGradient(value["gradient"], theme);
  var blendMode = parseBlendMode(value["blend_mode"]);

  return BoxDecoration(
    color: color,
    border: parseBorder(value["border"], theme),
    shape: shape,
    borderRadius: shape == BoxShape.circle ? null : borderRadius,
    backgroundBlendMode: color != null || gradient != null ? blendMode : null,
    boxShadow: parseBoxShadows(value["shadows"], theme),
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
  // If no custom properties are provided, return null
  if (!(color != null ||
      border != null ||
      borderRadius != null ||
      gradient != null ||
      shape != null ||
      boxShadow != null ||
      image != null)) {
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
  ImageProvider? image = parseImageProvider(src, context);
  if (image == null) return defaultValue;

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
