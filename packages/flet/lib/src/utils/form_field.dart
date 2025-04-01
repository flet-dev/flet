import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../controls/control_widget.dart';
import '../models/control.dart';
import 'borders.dart';
import 'box.dart';
import 'edge_insets.dart';
import 'icons.dart';
import 'numbers.dart';
import 'text.dart';
import 'time.dart';

enum FormFieldInputBorder { outline, underline, none }

FormFieldInputBorder? parseFormFieldInputBorder(String? value,
    [FormFieldInputBorder? defValue]) {
  if (value == null) {
    return defValue;
  }
  return FormFieldInputBorder.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

TextInputType? parseTextInputType(String? value, [TextInputType? defValue]) {
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
      return defValue;
  }
}

InputDecoration buildInputDecoration(BuildContext context, Control control,
    {Control? prefix,
    Control? prefixIcon,
    Control? suffix,
    Control? suffixIcon,
    Control? icon,
    Control? counter,
    Control? error,
    Control? helper,
    Control? label,
    Widget? customSuffix,
    int? valueLength,
    int? maxLength,
    bool focused = false,
    bool disabled = false,
    bool? adaptive}) {
  FormFieldInputBorder inputBorder = parseFormFieldInputBorder(
    control.getString("border"),
    FormFieldInputBorder.outline,
  )!;
  var iconStr = parseIcon(control.getString("icon"));
  var prefixIconData = parseIcon(control.getString("prefixIcon"));
  var prefixIconWidget = prefixIcon != null
      ? ControlWidget(control: prefixIcon)
      : (prefixIconData != null ? Icon(prefixIconData) : null);
  var suffixIconData = parseIcon(control.getString("suffixIcon"));
  var suffixIconWidget = suffixIcon != null
      ? ControlWidget(control: suffixIcon)
      : (suffixIconData != null ? Icon(suffixIconData) : null);
  var prefixText = control.getString("prefixText");
  var suffixText = control.getString("suffixText");

  var bgcolor = control.getColor("bgcolor", context);
  var focusedBgcolor = control.getColor("focusedBgcolor", context);
  var fillColor = control.getColor("fillColor", context);
  var hoverColor = control.getColor("hoverColor", context);
  var borderColor = control.getColor("borderColor", context);

  var borderRadius = parseBorderRadius(control, "borderRadius");
  var focusedBorderColor = control.getColor("focusedBorderColor", context);
  var borderWidth = control.getDouble("borderWidth");
  var focusedBorderWidth = control.getDouble("focusedBorderWidth");

  var counterText = control
      .getString("counterText", "")
      ?.replaceAll("{value_length}", valueLength.toString())
      .replaceAll("{max_length}", maxLength?.toString() ?? "None")
      .replaceAll("{symbols_left}",
          "${maxLength == null ? 'None' : (maxLength - (valueLength ?? 0))}");

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
      enabled: !disabled,
      contentPadding: parseEdgeInsets(control, "contentPadding"),
      isDense: control.getBool("dense"),
      label: label != null
          ? ControlWidget(control: label)
          : control.getString("label") != null
              ? Text(control.getString("label")!)
              : null,
      labelStyle: parseTextStyle(Theme.of(context), control, "labelStyle"),
      border: border,
      enabledBorder: border,
      focusedBorder: focusedBorder,
      hoverColor: hoverColor,
      icon: icon != null
          ? ControlWidget(control: icon)
          : iconStr != null
              ? Icon(iconStr)
              : null,
      filled: control.getBool("filled", false)!,
      fillColor: fillColor ?? (focused ? focusedBgcolor ?? bgcolor : bgcolor),
      hintText: control.getString("hintText"),
      hintStyle: parseTextStyle(Theme.of(context), control, "hintStyle"),
      helperText: control.getString("helperText"),
      helperStyle: parseTextStyle(Theme.of(context), control, "helperStyle"),
      counterText: counterText,
      counterStyle: parseTextStyle(Theme.of(context), control, "counterStyle"),
      counter: counter != null ? ControlWidget(control: counter) : null,
      error: error != null ? ControlWidget(control: error) : null,
      helper: helper != null ? ControlWidget(control: helper) : null,
      constraints: parseBoxConstraints(control, "sizeConstraints"),
      isCollapsed: control.getBool("collapsed"),
      prefixIconConstraints:
          parseBoxConstraints(control, "prefixIconConstraints"),
      suffixIconConstraints:
          parseBoxConstraints(control, "suffixIconConstraints"),
      focusColor: control.getColor("focusColor", context),
      errorMaxLines: control.getInt("errorMaxLines"),
      alignLabelWithHint: control.getBool("alignLabelWithHint"),
      errorText: control.getString("errorText"),
      errorStyle: parseTextStyle(Theme.of(context), control, "errorStyle"),
      prefixIcon: prefixIconWidget,
      prefixText:
          prefix == null ? prefixText : null, // ignored if prefix is set
      hintFadeDuration: parseDuration(control, "hintFadeDuration"),
      hintMaxLines: control.getInt("hintMaxLines"),
      helperMaxLines: control.getInt("helperMaxLines"),
      prefixStyle: parseTextStyle(Theme.of(context), control, "prefixStyle"),
      prefix: prefix != null ? ControlWidget(control: prefix) : null,
      suffix: suffix != null ? ControlWidget(control: suffix) : null,
      suffixIcon: suffixIconWidget ?? customSuffix,
      suffixText:
          suffix == null ? suffixText : null, // ignored if suffix is set
      suffixStyle: parseTextStyle(Theme.of(context), control, "suffixStyle"));
}

OverlayVisibilityMode? parseVisibilityMode(String? value,
    [OverlayVisibilityMode? defValue]) {
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
  return defValue;
}

StrutStyle? parseStrutStyle(Control control, String propName) {
  dynamic j;
  var v = control.getString(propName, null);
  if (v == null) {
    return null;
  }
  j = json.decode(v);
  return strutStyleFromJson(j);
}

StrutStyle? strutStyleFromJson(Map<String, dynamic>? json) {
  if (json == null) {
    return null;
  }

  return StrutStyle(
    fontSize: parseDouble(json["size"]),
    fontWeight: getFontWeight(json["weight"]),
    fontStyle: parseBool(json["italic"], false)! ? FontStyle.italic : null,
    fontFamily: json["font_family"],
    height: parseDouble(json["height"]),
    leading: parseDouble(json["leading"]),
    forceStrutHeight: parseBool(json["force_strut_height"]),
  );
}
