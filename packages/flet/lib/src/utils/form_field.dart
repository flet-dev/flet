import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

//import '../controls/control_widget.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import 'borders.dart';
import 'box.dart';
import 'edge_insets.dart';
//import 'icons.dart';
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

InputDecoration buildInputDecoration(BuildContext context, Control control,
    {
    //Control? prefix,
    Widget? prefix,
    //Control? prefixIcon,
    Widget? prefixIcon,
    //Control? suffix,
    Widget? suffix,
    //Control? suffixIcon,
    Widget? suffixIcon,
    //Control? icon,
    Widget? icon,
    //Control? counter,
    Widget? counter,
    //Control? error,
    Widget? error,
    //Control? helper,
    Widget? helper,
    //Control? label,
    Widget? label,
    //Widget? customSuffix,
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
  //var iconStr = parseIcon(control.getString("icon"));
  //var prefixIconData = parseIcon(control.getString("prefix_icon"));
  // var prefixIconWidget = prefixIcon != null
  //     ? ControlWidget(control: prefixIcon)
  //     : (prefixIconData != null ? Icon(prefixIconData) : null);
  //var suffixIconData = parseIcon(control.getString("suffix_icon"));
  // var suffixIconWidget = suffixIcon != null
  //     ? ControlWidget(control: suffixIcon)
  //     : (suffixIconData != null ? Icon(suffixIconData) : null);
  var prefixText = control.getString("prefix_text");
  var suffixText = control.getString("suffix_text");

  var bgcolor = control.getColor("bgcolor", context);
  var focusedBgcolor = control.getColor("focused_bgcolor", context);
  var fillColor = control.getColor("fill_color", context);
  var hoverColor = control.getColor("hover_color", context);
  var borderColor = control.getColor("border_color", context);

  var borderRadius = control.getBorderRadius("border_radius");
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
      contentPadding: control.getEdgeInsets("content_padding"),
      isDense: control.getBool("dense"),
      // label: label != null
      //     ? ControlWidget(control: label)
      //     : control.getString("label") != null
      //         ? Text(control.getString("label")!)
      //         : null,
      label: label,
      labelStyle: control.getTextStyle("label_style", Theme.of(context)),
      border: border,
      enabledBorder: border,
      focusedBorder: focusedBorder,
      hoverColor: hoverColor,
      // icon: icon != null
      //     ? ControlWidget(control: icon)
      //     : iconStr != null
      //         ? Icon(iconStr)
      //         : null,
      icon: icon,
      filled: control.getBool("filled", false)!,
      fillColor: fillColor ?? (focused ? (focusedBgcolor ?? bgcolor) : bgcolor),
      hintText: control.getString("hint_text"),
      hintStyle: control.getTextStyle("hint_style", Theme.of(context)),
      helperText: control.getString("helper_text"),
      helperStyle: control.getTextStyle("helper_style", Theme.of(context)),
      counterText: counterText,
      counterStyle: control.getTextStyle("counter_style", Theme.of(context)),
      //counter: counter != null ? ControlWidget(control: counter) : null,
      counter: counter,
      //error: error != null ? ControlWidget(control: error) : null,
      error: error,
      //helper: helper != null ? ControlWidget(control: helper) : null,
      helper: helper,
      constraints: control.getBoxConstraints("size_constraints"),
      isCollapsed: control.getBool("collapsed"),
      prefixIconConstraints:
          control.getBoxConstraints("prefix_icon_constraints"),
      suffixIconConstraints:
          control.getBoxConstraints("suffix_icon_constraints"),
      focusColor: control.getColor("focus_color", context),
      errorMaxLines: control.getInt("error_max_lines"),
      alignLabelWithHint: control.getBool("align_label_with_hint"),
      errorText: control.getString("error_text"),
      errorStyle: control.getTextStyle("error_style", Theme.of(context)),
      prefixIcon: prefixIcon,
      //prefixText: prefix == null ? prefixText : null,
      prefixText: prefixText,
      hintFadeDuration: control.getDuration("hint_fade_duration"),
      hintMaxLines: control.getInt("hint_max_lines"),
      helperMaxLines: control.getInt("helper_max_lines"),
      prefixStyle: control.getTextStyle("prefix_style", Theme.of(context)),
      //prefix: prefix != null ? ControlWidget(control: prefix) : null,
      prefix: prefix,
      //suffix: suffix != null ? ControlWidget(control: suffix) : null,
      suffix: suffix,
      suffixIcon: suffixIcon ?? customSuffix,
      suffixText: suffix == null ? suffixText : null,
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
