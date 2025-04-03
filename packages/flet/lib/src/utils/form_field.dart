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
  var prefixIconData = parseIcon(control.getString("prefix_icon"));
  var prefixIconWidget = prefixIcon != null
      ? ControlWidget(control: prefixIcon)
      : (prefixIconData != null ? Icon(prefixIconData) : null);
  var suffixIconData = parseIcon(control.getString("suffix_icon"));
  var suffixIconWidget = suffixIcon != null
      ? ControlWidget(control: suffixIcon)
      : (suffixIconData != null ? Icon(suffixIconData) : null);
  var prefixText = control.getString("prefix_text");
  var suffixText = control.getString("suffix_text");

  var bgcolor = control.getColor("bgcolor", context);
  var focusedBgcolor = control.getColor("focused_bgcolor", context);
  var fillColor = control.getColor("fill_color", context);
  var hoverColor = control.getColor("hover_color", context);
  var borderColor = control.getColor("border_color", context);

  var borderRadius = parseBorderRadius(control, "border_radius");
  var focusedBorderColor = control.getColor("focused_border_color", context);
  var borderWidth = control.getDouble("border_width");
  var focusedBorderWidth = control.getDouble("focused_border_width");

  var counterText = control
      .getString("counter_text", "")
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
      contentPadding: parseEdgeInsets(control, "content_padding"),
      isDense: control.getBool("dense"),
      label: label != null
          ? ControlWidget(control: label)
          : control.getString("label") != null
              ? Text(control.getString("label")!)
              : null,
      labelStyle: parseTextStyle(Theme.of(context), control, "label_style"),
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
      hintText: control.getString("hint_text"),
      hintStyle: parseTextStyle(Theme.of(context), control, "hint_style"),
      helperText: control.getString("helper_text"),
      helperStyle: parseTextStyle(Theme.of(context), control, "helper_style"),
      counterText: counterText,
      counterStyle: parseTextStyle(Theme.of(context), control, "counter_style"),
      counter: counter != null ? ControlWidget(control: counter) : null,
      error: error != null ? ControlWidget(control: error) : null,
      helper: helper != null ? ControlWidget(control: helper) : null,
      constraints: parseBoxConstraints(control, "size_constraints"),
      isCollapsed: control.getBool("collapsed"),
      prefixIconConstraints:
          parseBoxConstraints(control, "prefix_icon_constraints"),
      suffixIconConstraints:
          parseBoxConstraints(control, "suffix_icon_constraints"),
      focusColor: control.getColor("focus_color", context),
      errorMaxLines: control.getInt("error_max_lines"),
      alignLabelWithHint: control.getBool("align_label_with_hint"),
      errorText: control.getString("error_text"),
      errorStyle: parseTextStyle(Theme.of(context), control, "error_style"),
      prefixIcon: prefixIconWidget,
      prefixText: prefix == null ? prefixText : null,
      hintFadeDuration: parseDuration(control.get("hint_fade_duration")),
      hintMaxLines: control.getInt("hint_max_lines"),
      helperMaxLines: control.getInt("helper_max_lines"),
      prefixStyle: parseTextStyle(Theme.of(context), control, "prefix_style"),
      prefix: prefix != null ? ControlWidget(control: prefix) : null,
      suffix: suffix != null ? ControlWidget(control: suffix) : null,
      suffixIcon: suffixIconWidget ?? customSuffix,
      suffixText: suffix == null ? suffixText : null,
      suffixStyle: parseTextStyle(Theme.of(context), control, "suffix_style"));
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
  var v = control.get(propName);
  if (v == null) {
    return null;
  }
  return strutStyleFromJson(v);
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
