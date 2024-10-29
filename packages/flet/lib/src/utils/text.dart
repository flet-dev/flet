import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../models/control_tree_view_model.dart';
import '../utils/box.dart';
import '../utils/drawing.dart';
import '../utils/numbers.dart';
import 'colors.dart';
import 'launch_url.dart';
import 'material_state.dart';

TextStyle? getTextStyle(BuildContext context, String styleName) {
  var textTheme = Theme.of(context).textTheme;
  switch (styleName.toLowerCase()) {
    case "displaylarge":
      return textTheme.displayLarge;
    case "displaymedium":
      return textTheme.displayMedium;
    case "displaysmall":
      return textTheme.displaySmall;
    case "headlinelarge":
      return textTheme.headlineLarge;
    case "headlinemedium":
      return textTheme.headlineMedium;
    case "headlinesmall":
      return textTheme.headlineSmall;
    case "titlelarge":
      return textTheme.titleLarge;
    case "titlemedium":
      return textTheme.titleMedium;
    case "titlesmall":
      return textTheme.titleSmall;
    case "labellarge":
      return textTheme.labelLarge;
    case "labelmedium":
      return textTheme.labelMedium;
    case "labelsmall":
      return textTheme.labelSmall;
    case "bodylarge":
      return textTheme.bodyLarge;
    case "bodymedium":
      return textTheme.bodyMedium;
    case "bodysmall":
      return textTheme.bodySmall;
  }
  return null;
}

FontWeight? getFontWeight(String? weightName, [FontWeight? defaultWeight]) {
  switch (weightName?.toLowerCase()) {
    case "normal":
      return FontWeight.normal;
    case "bold":
      return FontWeight.bold;
    case "w100":
      return FontWeight.w100;
    case "w200":
      return FontWeight.w200;
    case "w300":
      return FontWeight.w300;
    case "w400":
      return FontWeight.w400;
    case "w500":
      return FontWeight.w500;
    case "w600":
      return FontWeight.w600;
    case "w700":
      return FontWeight.w700;
    case "w800":
      return FontWeight.w800;
    case "w900":
      return FontWeight.w900;
    default:
      return defaultWeight;
  }
}

List<InlineSpan> parseTextSpans(
    ThemeData theme,
    ControlTreeViewModel viewModel,
    bool parentDisabled,
    void Function(String, String, String)? sendControlEvent) {
  return viewModel.children
      .map((c) => parseInlineSpan(theme, c, parentDisabled, sendControlEvent))
      .whereNotNull()
      .toList();
}

InlineSpan? parseInlineSpan(
    ThemeData theme,
    ControlTreeViewModel spanViewModel,
    bool parentDisabled,
    void Function(String, String, String)? sendControlEvent) {
  if (spanViewModel.control.type == "textspan") {
    bool disabled = spanViewModel.control.isDisabled || parentDisabled;
    var onClick = spanViewModel.control.attrBool("onClick", false)!;
    String url = spanViewModel.control.attrString("url", "")!;
    String? urlTarget = spanViewModel.control.attrString("urlTarget");
    return TextSpan(
      text: spanViewModel.control.attrString("text"),
      style: parseTextStyle(theme, spanViewModel.control, "style"),
      spellOut: spanViewModel.control.attrBool("spellOut"),
      semanticsLabel: spanViewModel.control.attrString("semanticsLabel"),
      children: parseTextSpans(
          theme, spanViewModel, parentDisabled, sendControlEvent),
      mouseCursor: onClick && !disabled && sendControlEvent != null
          ? SystemMouseCursors.click
          : null,
      recognizer:
          (onClick || url != "") && !disabled && sendControlEvent != null
              ? (TapGestureRecognizer()
                ..onTap = () {
                  debugPrint("TextSpan ${spanViewModel.control.id} clicked!");
                  if (url != "") {
                    openWebBrowser(url, webWindowName: urlTarget);
                  }
                  if (onClick) {
                    sendControlEvent(spanViewModel.control.id, "click", "");
                  }
                })
              : null,
      onEnter: spanViewModel.control.attrBool("onEnter", false)! &&
              !disabled &&
              sendControlEvent != null
          ? (event) {
              debugPrint("TextSpan ${spanViewModel.control.id} entered!");
              sendControlEvent(spanViewModel.control.id, "enter", "");
            }
          : null,
      onExit: spanViewModel.control.attrBool("onExit", false)! &&
              !disabled &&
              sendControlEvent != null
          ? (event) {
              debugPrint("TextSpan ${spanViewModel.control.id} exited!");
              sendControlEvent(spanViewModel.control.id, "exit", "");
            }
          : null,
    );
  }
  return null;
}

TextAlign? parseTextAlign(String? value, [TextAlign? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return TextAlign.values.firstWhereOrNull(
          (a) => a.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TextOverflow? parseTextOverflow(String? value, [TextOverflow? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return TextOverflow.values.firstWhereOrNull(
          (a) => a.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TextCapitalization? parseTextCapitalization(String? value,
    [TextCapitalization? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return TextCapitalization.values.firstWhereOrNull(
          (a) => a.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TextBaseline? parseTextBaseline(String? value, [TextBaseline? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return TextBaseline.values.firstWhereOrNull(
          (a) => a.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TextStyle? parseTextStyle(ThemeData theme, Control control, String propName) {
  dynamic j;
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }
  j = json.decode(v);
  return textStyleFromJson(theme, j);
}

TextStyle? textStyleFromJson(ThemeData theme, Map<String, dynamic>? json) {
  if (json == null) {
    return null;
  }

  var fontWeight = json["weight"];

  List<FontVariation>? variations;
  if (fontWeight != null && fontWeight.startsWith("w")) {
    variations = [
      FontVariation('wght', parseDouble(fontWeight.substring(1), 0)!)
    ];
  }

  List<TextDecoration> decorations = [];
  var decor = parseInt(json["decoration"], 0)!;
  if (decor & 0x1 > 0) {
    decorations.add(TextDecoration.underline);
  }
  if (decor & 0x2 > 0) {
    decorations.add(TextDecoration.overline);
  }
  if (decor & 0x4 > 0) {
    decorations.add(TextDecoration.lineThrough);
  }

  return TextStyle(
    fontSize: parseDouble(json["size"]),
    fontWeight: getFontWeight(fontWeight),
    fontStyle: parseBool(json["italic"], false)! ? FontStyle.italic : null,
    fontFamily: json["font_family"],
    fontVariations: variations,
    height: parseDouble(json["height"]),
    decoration:
        decorations.isNotEmpty ? TextDecoration.combine(decorations) : null,
    decorationStyle: json["decoration_style"] != null
        ? TextDecorationStyle.values.firstWhereOrNull((v) =>
            v.name.toLowerCase() == json["decoration_style"].toLowerCase())
        : null,
    decorationColor: parseColor(theme, json["decoration_color"]),
    decorationThickness: parseDouble(json["decoration_thickness"]),
    color: parseColor(theme, json["color"]),
    backgroundColor: parseColor(theme, json["bgcolor"]),
    shadows: json["shadow"] != null
        ? boxShadowsFromJSON(theme, json["shadow"])
        : null,
    foreground: json["foreground"] != null
        ? paintFromJSON(theme, json["foreground"])
        : null,
    letterSpacing: parseDouble(json['letter_spacing']),
    overflow: parseTextOverflow(json['overflow']),
    wordSpacing: parseDouble(json['word_spacing']),
    textBaseline: parseTextBaseline(json['text_baseline']),
  );
}

WidgetStateProperty<TextStyle?>? parseWidgetStateTextStyle(
    ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName);
  if (v == null) {
    return null;
  }
  return getWidgetStateProperty<TextStyle?>(
      jsonDecode(v), (jv) => textStyleFromJson(theme, jv), null);
}
