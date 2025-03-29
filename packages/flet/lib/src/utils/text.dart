import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
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
    List<Control> spans,
    bool parentDisabled,
    void Function(Control, String, String)? sendControlEvent) {
  return spans
      .map((span) =>
          parseInlineSpan(theme, span, parentDisabled, sendControlEvent))
      .nonNulls
      .toList();
}

InlineSpan? parseInlineSpan(ThemeData theme, Control span, bool parentDisabled,
    void Function(Control, String, String)? sendControlEvent) {
  span.notifyParent = true;
  bool disabled = span.disabled || parentDisabled;
  var onClick = span.get<bool>("on_click", false)!;
  String url = span.get<String>("url", "")!;
  String? urlTarget = span.get<String>("url_target");
  return TextSpan(
    text: span.get<String>("text"),
    style: parseTextStyle(theme, span, "style"),
    spellOut: span.get<bool>("spell_out"),
    semanticsLabel: span.get<String>("semantics_label"),
    children: parseTextSpans(
        theme, span.children("spans"), parentDisabled, sendControlEvent),
    mouseCursor: onClick && !disabled && sendControlEvent != null
        ? SystemMouseCursors.click
        : null,
    recognizer: (onClick || url != "") && !disabled && sendControlEvent != null
        ? (TapGestureRecognizer()
          ..onTap = () {
            if (url != "") {
              openWebBrowser(url, webWindowName: urlTarget);
            }
            if (onClick) {
              sendControlEvent(span, "click", "");
            }
          })
        : null,
    onEnter: span.get<bool>("on_enter", false)! &&
            !disabled &&
            sendControlEvent != null
        ? (event) {
            sendControlEvent(span, "enter", "");
          }
        : null,
    onExit: span.get<bool>("on_exit", false)! &&
            !disabled &&
            sendControlEvent != null
        ? (event) {
            sendControlEvent(span, "exit", "");
          }
        : null,
  );
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
  var v = control.get(propName);
  if (v == null) {
    return null;
  }
  return textStyleFromJson(theme, Map<String, dynamic>.from(v));
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
  var v = control.get<String>(propName);
  if (v == null) {
    return null;
  }
  return getWidgetStateProperty<TextStyle?>(
      jsonDecode(v), (jv) => textStyleFromJson(theme, jv), null);
}
