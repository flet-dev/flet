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

List<TextSpan> parseTextSpans(
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

TextSpan? parseInlineSpan(ThemeData theme, Control span, bool parentDisabled,
    void Function(Control, String, String)? sendControlEvent) {
  span.notifyParent = true;
  bool disabled = span.disabled || parentDisabled;
  var onClick = span.getBool("on_click", false)!;
  String url = span.getString("url", "")!;
  String? urlTarget = span.getString("url_target");
  return TextSpan(
    text: span.getString("text"),
    style: parseTextStyle(span.get("style"), theme),
    spellOut: span.getBool("spell_out"),
    semanticsLabel: span.getString("semantics_label"),
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
    onEnter: span.getBool("on_enter", false)! &&
            !disabled &&
            sendControlEvent != null
        ? (event) {
            sendControlEvent(span, "enter", "");
          }
        : null,
    onExit:
        span.getBool("on_exit", false)! && !disabled && sendControlEvent != null
            ? (event) {
                sendControlEvent(span, "exit", "");
              }
            : null,
  );
}

TextAlign? parseTextAlign(String? value, [TextAlign? defaultValue]) {
  if (value == null) return defaultValue;
  return TextAlign.values.firstWhereOrNull(
          (a) => a.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TextOverflow? parseTextOverflow(String? value, [TextOverflow? defaultValue]) {
  if (value == null) return defaultValue;
  return TextOverflow.values.firstWhereOrNull(
          (a) => a.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TextDecorationStyle? parseTextDecorationStyle(String? value,
    [TextDecorationStyle? defaultValue]) {
  if (value == null) return defaultValue;
  return TextDecorationStyle.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TextCapitalization? parseTextCapitalization(String? value,
    [TextCapitalization? defaultValue]) {
  if (value == null) return defaultValue;
  return TextCapitalization.values.firstWhereOrNull(
          (a) => a.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TextBaseline? parseTextBaseline(String? value, [TextBaseline? defaultValue]) {
  if (value == null) return defaultValue;
  return TextBaseline.values.firstWhereOrNull(
          (a) => a.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TextStyle? parseTextStyle(dynamic value, ThemeData theme,
    [TextStyle? defaultValue]) {
  if (value == null) return defaultValue;
  var fontWeight = value["weight"];

  List<FontVariation>? variations;
  if (fontWeight != null && fontWeight.startsWith("w")) {
    variations = [
      FontVariation('wght', parseDouble(fontWeight.substring(1), 0)!)
    ];
  }

  List<TextDecoration> decorations = [];
  var decor = parseInt(value["decoration"], 0)!;
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
    fontSize: parseDouble(value["size"]),
    fontWeight: getFontWeight(fontWeight),
    fontStyle: parseBool(value["italic"], false)! ? FontStyle.italic : null,
    fontFamily: value["font_family"],
    fontVariations: variations,
    height: parseDouble(value["height"]),
    decoration:
        decorations.isNotEmpty ? TextDecoration.combine(decorations) : null,
    decorationStyle: parseTextDecorationStyle(value["decoration_style"]),
    decorationColor: parseColor(value["decoration_color"], theme),
    decorationThickness: parseDouble(value["decoration_thickness"]),
    color: parseColor(value["color"], theme),
    backgroundColor: parseColor(value["bgcolor"], theme),
    shadows: parseBoxShadows(value["shadow"], theme),
    foreground: parsePaint(value["foreground"], theme),
    letterSpacing: parseDouble(value['letter_spacing']),
    overflow: parseTextOverflow(value['overflow']),
    wordSpacing: parseDouble(value['word_spacing']),
    textBaseline: parseTextBaseline(value['text_baseline']),
  );
}

WidgetStateProperty<TextStyle?>? parseWidgetStateTextStyle(
    dynamic value, ThemeData theme,
    {TextStyle? defaultTextStyle,
    WidgetStateProperty<TextStyle?>? defaultValue}) {
  if (value == null) return defaultValue;
  return getWidgetStateProperty<TextStyle?>(
      value, (jv) => parseTextStyle(theme, jv), defaultTextStyle);
}

extension TextParsers on Control {
  TextStyle? getTextStyle(String propertyName, ThemeData theme,
      [TextStyle? defaultValue]) {
    return parseTextStyle(get(propertyName), theme, defaultValue);
  }

  TextAlign? getTextAlign(String propertyName, [TextAlign? defaultValue]) {
    return parseTextAlign(get(propertyName), defaultValue);
  }

  TextOverflow? getTextOverflow(String propertyName,
      [TextOverflow? defaultValue]) {
    return parseTextOverflow(get(propertyName), defaultValue);
  }

  TextDecorationStyle? getTextDecorationStyle(String propertyName,
      [TextDecorationStyle? defaultValue]) {
    return parseTextDecorationStyle(get(propertyName), defaultValue);
  }

  TextCapitalization? getTextCapitalization(String propertyName,
      [TextCapitalization? defaultValue]) {
    return parseTextCapitalization(get(propertyName), defaultValue);
  }

  TextBaseline? getTextBaseline(String propertyName,
      [TextBaseline? defaultValue]) {
    return parseTextBaseline(get(propertyName), defaultValue);
  }

  WidgetStateProperty<TextStyle?>? getWidgetStateTextStyle(
      String propertyName, ThemeData theme,
      {TextStyle? defaultTextStyle,
      WidgetStateProperty<TextStyle?>? defaultValue}) {
    return parseWidgetStateTextStyle(get(propertyName), theme,
        defaultTextStyle: defaultTextStyle, defaultValue: defaultValue);
  }
}

extension TextSelectionExtension on TextSelection {
  Map<String, dynamic> toMap() => {
        "start": start,
        "end": end,
        "base_offset": baseOffset,
        "extent_offset": extentOffset,
        "affinity": affinity.name,
        "directional": isDirectional,
        "collapsed": isCollapsed,
        "valid": isValid,
        "normalized": isNormalized,
      };
}
