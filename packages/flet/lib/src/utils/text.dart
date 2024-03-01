import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../models/control_tree_view_model.dart';
import '../utils/drawing.dart';
import '../utils/numbers.dart';
import '../utils/shadows.dart';
import 'colors.dart';
import 'launch_url.dart';

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

FontWeight? getFontWeight(String weightName) {
  switch (weightName.toLowerCase()) {
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
  }
  return null;
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

TextAlign? parseTextAlign(String align, [TextAlign? defaultAlign]) {
  return TextAlign.values.firstWhereOrNull(
          (a) => a.name.toLowerCase() == align.toLowerCase()) ??
      defaultAlign;
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

TextStyle textStyleFromJson(ThemeData theme, Map<String, dynamic> json) {
  var fontWeight = json["weight"];

  List<FontVariation>? variations;
  if (fontWeight != null && fontWeight.startsWith("w")) {
    variations = [FontVariation('wght', parseDouble(fontWeight.substring(1)))];
  }

  List<TextDecoration> decorations = [];
  var decor = parseInt(json["decoration"]);
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
      fontSize: json["size"] != null ? parseDouble(json["size"]) : null,
      fontWeight: fontWeight != null ? getFontWeight(fontWeight) : null,
      fontStyle: (json["italic"] != null)
          ? (parseBool(json["italic"]) ? FontStyle.italic : null)
          : null,
      fontFamily: json["font_family"],
      fontVariations: variations,
      height: json["height"] != null ? parseDouble(json["height"]) : null,
      decoration:
          decorations.isNotEmpty ? TextDecoration.combine(decorations) : null,
      decorationStyle: json["decoration_style"] != null
          ? TextDecorationStyle.values.firstWhereOrNull((v) =>
              v.name.toLowerCase() == json["decoration_style"].toLowerCase())
          : null,
      decorationColor: json["decoration_color"] != null
          ? HexColor.fromString(theme, json["decoration_color"] ?? "")
          : null,
      decorationThickness: json["decoration_thickness"] != null
          ? parseDouble(json["decoration_thickness"])
          : null,
      color: json["color"] != null
          ? HexColor.fromString(theme, json["color"] ?? "")
          : null,
      backgroundColor: json["bgcolor"] != null
          ? HexColor.fromString(theme, json["bgcolor"] ?? "")
          : null,
      shadows: json["shadow"] != null
          ? boxShadowsFromJSON(theme, json["shadow"])
          : null,
      foreground: json["foreground"] != null
          ? paintFromJSON(theme, json["foreground"])
          : null,
      letterSpacing: json['letter_spacing'] != null
          ? parseDouble(json['letter_spacing'])
          : null);
}
