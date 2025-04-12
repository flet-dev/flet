import 'package:collection/collection.dart';
import 'package:flet/src/extensions/control.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import 'borders.dart';
import 'box.dart';
import 'edge_insets.dart';
import 'numbers.dart';
import 'text.dart';
import 'time.dart';

enum FormFieldInputBorder { outline, underline, none }

FormFieldInputBorder? parseFormFieldInputBorder(String? value,
    [FormFieldInputBorder? defaultValue]) {
  if (value == null) return defaultValue;
  return FormFieldInputBorder.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TextInputType? parseTextInputType(String? value,
    [TextInputType? defaultValue]) {
  switch (value?.toLowerCase()) {
    case "datetime":
      return TextInputType.datetime;
    case "email":
      return TextInputType.emailAddress;
    case "multiline":
      return TextInputType.multiline;
    case "name":
      return TextInputType.name;
    case "none":
      return TextInputType.none;
    case "number":
      return TextInputType.number;
    case "phone":
      return TextInputType.phone;
    case "streetaddress":
      return TextInputType.streetAddress;
    case "text":
      return TextInputType.text;
    case "url":
      return TextInputType.url;
    case "visiblepassword":
      return TextInputType.visiblePassword;
    default:
      return defaultValue;
  }
}

InputDecoration buildInputDecoration(
  BuildContext context,
  Control control, {
  Widget? customSuffix,
  int? valueLength,
  int? maxLength,
  bool focused = false,
}) {
  FormFieldInputBorder inputBorder = parseFormFieldInputBorder(
    control.getString("border"),
    FormFieldInputBorder.outline,
  )!;
  var bgcolor = control.getColor("bgcolor", context);
  var focusedBgcolor = control.getColor("focused_bgcolor", context);
  var fillColor = control.getColor("fill_color", context);
  var hoverColor = control.getColor("hover_color", context);
  var borderColor = control.getColor("border_color", context);
  var borderRadius = control.getBorderRadius("border_radius");
  var focusedBorderColor = control.getColor("focused_border_color", context);
  var borderWidth = control.getDouble("border_width");
  var focusedBorderWidth = control.getDouble("focused_border_width");

  //counter
  String? counterText;
  Widget? counterWidget;
  var counter = control.get("counter");
  if (counter is Control) {
    counterWidget = control.buildWidget("counter");
  } else {
    counterText = control.getString("counter") ??
        control
            .getString("counter_text",
                "") // todo(0.73.0): remove "counter_text" in favor of "counter"
            ?.replaceAll("{value_length}", valueLength.toString())
            .replaceAll("{max_length}", maxLength?.toString() ?? "None")
            .replaceAll("{symbols_left}",
                "${maxLength == null ? 'None' : (maxLength - (valueLength ?? 0))}");
  }

  // error
  String? errorText;
  Widget? errorWidget;
  var error = control.get("error");
  if (error is Control) {
    errorWidget = control.buildWidget("error");
  } else {
    errorText = control.getString("error") ??
        control.getString(
            "error_text"); // todo(0.73.0): remove "error_text" in favor of "error"
  }
  // helper
  String? helperText;
  Widget? helperWidget;
  var helper = control.get("helper");
  if (helper is Control) {
    helperWidget = control.buildWidget("helper");
  } else {
    helperText = control.getString("helper") ??
        control.getString(
            "helper_text"); // todo(0.73.0): remove "helper_text" in favor of "helper"
  }

  // prefix
  String? prefixText;
  Widget? prefixWidget;
  var prefix = control.get("prefix");
  if (prefix is Control) {
    prefixWidget = control.buildWidget("prefix");
  } else {
    prefixText = control.getString("prefix") ??
        control.getString(
            "prefix_text"); // todo(0.73.0): remove "prefix_text" in favor of "prefix"
  }

  // suffix
  String? suffixText;
  Widget? suffixWidget;
  var suffix = control.get("suffix");
  if (suffix is Control) {
    suffixWidget = control.buildWidget("suffix");
  } else {
    suffixText = control.getString("suffix") ??
        control.getString(
            "suffix_text"); // todo(0.73.0): remove "suffix_text" in favor of "suffix"
  }

  InputBorder? border;
  if (inputBorder == FormFieldInputBorder.underline) {
    border = UnderlineInputBorder(
        borderSide: BorderSide(
            color: borderColor ?? const Color(0xFF000000),
            width: borderWidth ?? 1.0));
  } else if (inputBorder == FormFieldInputBorder.none) {
    border = InputBorder.none;
  } else if (inputBorder == FormFieldInputBorder.outline ||
      borderRadius != null ||
      borderColor != null ||
      borderWidth != null) {
    border = OutlineInputBorder(
        borderSide: BorderSide(
            color: borderColor ?? const Color(0xFF000000),
            width: borderWidth ?? 1.0));
    if (borderRadius != null) {
      border =
          (border as OutlineInputBorder).copyWith(borderRadius: borderRadius);
    }
    if (borderColor != null || borderWidth != null) {
      border = (border as OutlineInputBorder).copyWith(
          borderSide: borderWidth == 0
              ? BorderSide.none
              : BorderSide(
                  color: borderColor ??
                      Theme.of(context)
                          .colorScheme
                          .onSurface
                          .withAlpha((255.0 * 0.38).round()),
                  width: borderWidth ?? 1.0));
    }
  }

  InputBorder? focusedBorder;
  if (borderColor != null ||
      borderWidth != null ||
      focusedBorderColor != null ||
      focusedBorderWidth != null) {
    focusedBorder = border?.copyWith(
        borderSide: borderWidth == 0
            ? BorderSide.none
            : BorderSide(
                color: focusedBorderColor ??
                    borderColor ??
                    Theme.of(context).colorScheme.primary,
                width: focusedBorderWidth ?? borderWidth ?? 2.0));
  }

  return InputDecoration(
      enabled: !control.disabled,
      contentPadding: control.getEdgeInsets("content_padding"),
      isDense: control.getBool("dense"),
      label: control.buildTextOrWidget("label"),
      labelStyle: control.getTextStyle("label_style", Theme.of(context)),
      border: border,
      enabledBorder: border,
      focusedBorder: focusedBorder,
      hoverColor: hoverColor,
      icon: control.buildIconOrWidget("icon"),
      filled: control.getBool("filled", false)!,
      fillColor: fillColor ?? (focused ? (focusedBgcolor ?? bgcolor) : bgcolor),
      //hint
      hintText: control.getString("hint_text"),
      hintStyle: control.getTextStyle("hint_style", Theme.of(context)),
      hintFadeDuration: control.getDuration("hint_fade_duration"),
      hintMaxLines: control.getInt("hint_max_lines"),
      //helper
      helper: helperWidget,
      helperText: helperText,
      helperStyle: control.getTextStyle("helper_style", Theme.of(context)),
      helperMaxLines: control.getInt("helper_max_lines"),
      //counter
      counter: counterWidget,
      counterText: counterText,
      counterStyle: control.getTextStyle("counter_style", Theme.of(context)),
      //error
      error: errorWidget,
      errorText: errorText,
      errorStyle: control.getTextStyle("error_style", Theme.of(context)),
      errorMaxLines: control.getInt("error_max_lines"),
      constraints: control.getBoxConstraints("size_constraints"),
      isCollapsed: control.getBool("collapsed"),
      prefixIconConstraints:
          control.getBoxConstraints("prefix_icon_constraints"),
      suffixIconConstraints:
          control.getBoxConstraints("suffix_icon_constraints"),
      focusColor: control.getColor("focus_color", context),
      alignLabelWithHint: control.getBool("align_label_with_hint"),
      prefixIcon: control.buildIconOrWidget("prefix_icon"),
      //prefix
      prefix: prefixWidget,
      prefixText: prefixText,
      prefixStyle: control.getTextStyle("prefix_style", Theme.of(context)),
      suffixIcon: control.buildIconOrWidget("suffix_icon") ?? customSuffix,
      //suffix
      suffix: suffixWidget,
      suffixText: suffixText,
      suffixStyle: control.getTextStyle("suffix_style", Theme.of(context)));
}

OverlayVisibilityMode? parseOverlayVisibilityMode(String? value,
    [OverlayVisibilityMode? defaultValue]) {
  switch (value?.toLowerCase()) {
    case "never":
      return OverlayVisibilityMode.never;
    case "notediting":
      return OverlayVisibilityMode.notEditing;
    case "editing":
      return OverlayVisibilityMode.editing;
    case "always":
      return OverlayVisibilityMode.always;
  }
  return defaultValue;
}

StrutStyle? parseStrutStyle(dynamic value, [StrutStyle? defaultValue]) {
  if (value == null) return defaultValue;

  return StrutStyle(
    fontSize: parseDouble(value["size"]),
    fontWeight: getFontWeight(value["weight"]),
    fontStyle: parseBool(value["italic"], false)! ? FontStyle.italic : null,
    fontFamily: value["font_family"],
    height: parseDouble(value["height"]),
    leading: parseDouble(value["leading"]),
    forceStrutHeight: parseBool(value["force_strut_height"]),
  );
}

extension FormFieldParsers on Control {
  FormFieldInputBorder? getFormFieldInputBorder(String propertyName,
      [FormFieldInputBorder? defaultValue]) {
    return parseFormFieldInputBorder(get(propertyName), defaultValue);
  }

  TextInputType? getTextInputType(String propertyName,
      [TextInputType? defaultValue]) {
    return parseTextInputType(get(propertyName), defaultValue);
  }

  OverlayVisibilityMode? getOverlayVisibilityMode(String propertyName,
      [OverlayVisibilityMode? defaultValue]) {
    return parseOverlayVisibilityMode(get(propertyName), defaultValue);
  }

  StrutStyle? getStrutStyle(String propertyName, [StrutStyle? defaultValue]) {
    return parseStrutStyle(get(propertyName), defaultValue);
  }
}
