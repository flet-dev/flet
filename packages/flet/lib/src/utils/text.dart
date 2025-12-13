import 'dart:math';

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

TextStyle? parseTextThemeStyle(String? styleName, BuildContext context) {
  var textTheme = Theme.of(context).textTheme;
  final styles = <String, TextStyle?>{
    "displaylarge": textTheme.displayLarge,
    "displaymedium": textTheme.displayMedium,
    "displaysmall": textTheme.displaySmall,
    "headlinelarge": textTheme.headlineLarge,
    "headlinemedium": textTheme.headlineMedium,
    "headlinesmall": textTheme.headlineSmall,
    "titlelarge": textTheme.titleLarge,
    "titlemedium": textTheme.titleMedium,
    "titlesmall": textTheme.titleSmall,
    "labellarge": textTheme.labelLarge,
    "labelmedium": textTheme.labelMedium,
    "labelsmall": textTheme.labelSmall,
    "bodylarge": textTheme.bodyLarge,
    "bodymedium": textTheme.bodyMedium,
    "bodysmall": textTheme.bodySmall,
  };
  return styles[styleName?.toLowerCase()];
}

FontWeight? parseFontWeight(String? weightName, [FontWeight? defaultWeight]) {
  if (weightName == null) return defaultWeight;
  final weights = <String, FontWeight>{
    "normal": FontWeight.normal,
    "bold": FontWeight.bold,
    "w100": FontWeight.w100,
    "w200": FontWeight.w200,
    "w300": FontWeight.w300,
    "w400": FontWeight.w400,
    "w500": FontWeight.w500,
    "w600": FontWeight.w600,
    "w700": FontWeight.w700,
    "w800": FontWeight.w800,
    "w900": FontWeight.w900,
  };
  return weights[weightName.toLowerCase()] ?? defaultWeight;
}

List<TextSpan> parseTextSpans(List<Control> spans, ThemeData theme,
    [void Function(Control, String, [dynamic eventData])? sendControlEvent]) {
  return spans
      .map((span) => parseInlineSpan(span, theme, sendControlEvent))
      .nonNulls
      .toList();
}

TextSpan? parseInlineSpan(Control span, ThemeData theme,
    [void Function(Control, String, [dynamic eventData])? sendControlEvent]) {
  span.notifyParent = true;
  var onClick = span.getBool("on_click", false)!;
  var url = span.getUrl("url");

  return TextSpan(
    text: span.getString("text"),
    style: parseTextStyle(span.get("style"), theme),
    spellOut: span.getBool("spell_out"),
    semanticsLabel: span.getString("semantics_label"),
    children: parseTextSpans(span.children("spans"), theme, sendControlEvent),
    mouseCursor: onClick && !span.disabled && sendControlEvent != null
        ? SystemMouseCursors.click
        : null,
    recognizer:
        (onClick || url != null) && !span.disabled && sendControlEvent != null
            ? (TapGestureRecognizer()
              ..onTap = () {
                if (url != null) openWebBrowser(url);
                if (onClick) sendControlEvent(span, "click");
              })
            : null,
    onEnter: span.getBool("on_enter", false)! &&
            !span.disabled &&
            sendControlEvent != null
        ? (event) => sendControlEvent(span, "enter")
        : null,
    onExit: span.getBool("on_exit", false)! &&
            !span.disabled &&
            sendControlEvent != null
        ? (event) => sendControlEvent(span, "exit")
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

TextAffinity? parseTextAffinity(String? value, [TextAffinity? defaultValue]) {
  if (value == null) return defaultValue;
  return TextAffinity.values.firstWhereOrNull(
          (a) => a.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

List<FontVariation>? parseFontVariations(dynamic fontWeight,
    [List<FontVariation>? defaultValue]) {
  if (fontWeight != null &&
      fontWeight is String &&
      fontWeight.startsWith("w")) {
    return [FontVariation('wght', parseDouble(fontWeight.substring(1), 0)!)];
  }
  return defaultValue;
}

List<TextDecoration> parseTextDecorations(dynamic decorationValue) {
  List<TextDecoration> decorations = [];
  var decor = parseInt(decorationValue, 0)!;
  if (decor & 0x1 > 0) {
    decorations.add(TextDecoration.underline);
  }
  if (decor & 0x2 > 0) {
    decorations.add(TextDecoration.overline);
  }
  if (decor & 0x4 > 0) {
    decorations.add(TextDecoration.lineThrough);
  }
  return decorations;
}

TextStyle? parseTextStyle(dynamic value, ThemeData theme,
    [TextStyle? defaultValue]) {
  if (value == null) return defaultValue;

  var fontWeight = value["weight"];
  List<FontVariation>? variations = parseFontVariations(fontWeight);
  List<TextDecoration> decorations = parseTextDecorations(value["decoration"]);

  return TextStyle(
    fontSize: parseDouble(value["size"]),
    fontWeight: parseFontWeight(fontWeight),
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
      value, (jv) => parseTextStyle(jv, theme), defaultTextStyle);
}

TextSelection? parseTextSelection(
  dynamic value, {
  int? minOffset,
  int? maxOffset,
  TextSelection? defaultValue,
}) {
  if (value == null) return defaultValue;

  int baseOffset = parseInt(value['base_offset'], 0)!;
  int extentOffset = parseInt(value['extent_offset'], 0)!;

  // Clamp values if limits are provided
  if (minOffset != null) {
    baseOffset = max(baseOffset, minOffset);
    extentOffset = max(extentOffset, minOffset);
  }
  if (maxOffset != null) {
    baseOffset = min(baseOffset, maxOffset);
    extentOffset = min(extentOffset, maxOffset);
  }

  return TextSelection(
    baseOffset: baseOffset,
    extentOffset: extentOffset,
    affinity: parseTextAffinity(value['affinity'], TextAffinity.downstream)!,
    isDirectional: parseBool(value['directional'], false)!,
  );
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

  TextAffinity? getTextAffinity(String propertyName,
      [TextAffinity? defaultValue]) {
    return parseTextAffinity(get(propertyName), defaultValue);
  }

  TextSelection? getTextSelection(
    String propertyName, {
    int? minOffset,
    int? maxOffset,
    TextSelection? defaultValue,
  }) {
    return parseTextSelection(get(propertyName),
        minOffset: minOffset, maxOffset: maxOffset, defaultValue: defaultValue);
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
        "base_offset": baseOffset,
        "extent_offset": extentOffset,
        "affinity": affinity.name,
        "directional": isDirectional,
      };
}
