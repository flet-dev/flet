import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../controls/create_control.dart';
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
    control.attrString("border"),
    FormFieldInputBorder.outline,
  )!;
  var iconStr = parseIcon(control.attrString("icon"));
  var prefixIconData = parseIcon(control.attrString("prefixIcon"));
  var prefixIconWidget = prefixIcon != null
      ? createControl(control, prefixIcon.id, control.isDisabled,
          parentAdaptive: adaptive)
      : (prefixIconData != null ? Icon(prefixIconData) : null);
  var suffixIconData = parseIcon(control.attrString("suffixIcon"));
  var suffixIconWidget = suffixIcon != null
      ? createControl(control, suffixIcon.id, control.isDisabled,
          parentAdaptive: adaptive)
      : (suffixIconData != null ? Icon(suffixIconData) : null);
  var prefixText = control.attrString("prefixText");
  var suffixText = control.attrString("suffixText");

  var bgcolor = control.attrColor("bgcolor", context);
  var focusedBgcolor = control.attrColor("focusedBgcolor", context);
  var fillColor = control.attrColor("fillColor", context);
  var hoverColor = control.attrColor("hoverColor", context);
  var borderColor = control.attrColor("borderColor", context);

  var borderRadius = parseBorderRadius(control, "borderRadius");
  var focusedBorderColor = control.attrColor("focusedBorderColor", context);
  var borderWidth = control.attrDouble("borderWidth");
  var focusedBorderWidth = control.attrDouble("focusedBorderWidth");

  var counterText = control
      .attrString("counterText", "")
      ?.replaceAll("{value_length}", valueLength.toString())
      .replaceAll("{max_length}", maxLength?.toString() ?? "None")
      .replaceAll("{symbols_left}",
          "${maxLength == null ? 'None' : (maxLength - (valueLength ?? 0))}");

  InputBorder? border;
  if (inputBorder == FormFieldInputBorder.underline) {
    border = UnderlineInputBorder(
        borderSide: BorderSide(
            color: borderColor ?? Color(0xFF000000),
            width: borderWidth ?? 1.0));
  } else if (inputBorder == FormFieldInputBorder.none) {
    border = InputBorder.none;
  } else if (inputBorder == FormFieldInputBorder.outline ||
      borderRadius != null ||
      borderColor != null ||
      borderWidth != null) {
    border = OutlineInputBorder(
        borderSide: BorderSide(
            color: borderColor ?? Color(0xFF000000),
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
                      Theme.of(context).colorScheme.onSurface.withOpacity(0.38),
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
      isDense: control.attrBool("dense"),
      label: label != null
          ? createControl(control, label.id, control.isDisabled,
              parentAdaptive: adaptive)
          : control.attrString("label") != null
              ? Text(control.attrString("label")!)
              : null,
      labelStyle: parseTextStyle(Theme.of(context), control, "labelStyle"),
      border: border,
      enabledBorder: border,
      focusedBorder: focusedBorder,
      hoverColor: hoverColor,
      icon: icon != null
          ? createControl(control, icon.id, control.isDisabled,
              parentAdaptive: adaptive)
          : iconStr != null
              ? Icon(iconStr)
              : null,
      filled: control.attrBool("filled", false)!,
      fillColor: fillColor ?? (focused ? focusedBgcolor ?? bgcolor : bgcolor),
      hintText: control.attrString("hintText"),
      hintStyle: parseTextStyle(Theme.of(context), control, "hintStyle"),
      helperText: control.attrString("helperText"),
      helperStyle: parseTextStyle(Theme.of(context), control, "helperStyle"),
      counterText: counterText,
      counterStyle: parseTextStyle(Theme.of(context), control, "counterStyle"),
      counter: counter != null
          ? createControl(control, counter.id, control.isDisabled,
              parentAdaptive: adaptive)
          : null,
      error: error != null
          ? createControl(control, error.id, control.isDisabled,
              parentAdaptive: adaptive)
          : null,
      helper: helper != null
          ? createControl(control, helper.id, control.isDisabled,
              parentAdaptive: adaptive)
          : null,
      constraints: parseBoxConstraints(control, "sizeConstraints"),
      isCollapsed: control.attrBool("collapsed"),
      prefixIconConstraints:
          parseBoxConstraints(control, "prefixIconConstraints"),
      suffixIconConstraints:
          parseBoxConstraints(control, "suffixIconConstraints"),
      focusColor: control.attrColor("focusColor", context),
      errorMaxLines: control.attrInt("errorMaxLines"),
      alignLabelWithHint: control.attrBool("alignLabelWithHint"),
      errorText: control.attrString("errorText"),
      errorStyle: parseTextStyle(Theme.of(context), control, "errorStyle"),
      prefixIcon: prefixIconWidget,
      prefixText:
          prefix == null ? prefixText : null, // ignored if prefix is set
      hintFadeDuration: parseDuration(control, "hintFadeDuration"),
      hintMaxLines: control.attrInt("hintMaxLines"),
      helperMaxLines: control.attrInt("helperMaxLines"),
      prefixStyle: parseTextStyle(Theme.of(context), control, "prefixStyle"),
      prefix: prefix != null
          ? createControl(control, prefix.id, control.isDisabled,
              parentAdaptive: adaptive)
          : null,
      suffix: suffix != null
          ? createControl(control, suffix.id, control.isDisabled,
              parentAdaptive: adaptive)
          : null,
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
  var v = control.attrString(propName, null);
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
