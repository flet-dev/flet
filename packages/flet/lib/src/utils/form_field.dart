import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../controls/create_control.dart';
import '../models/control.dart';
import 'borders.dart';
import 'edge_insets.dart';
import 'icons.dart';
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
    Control? suffix,
    Control? counter,
    Control? helper,
    Control? error,
    Widget? customSuffix,
    bool focused = false,
    bool disabled = false,
    bool? adaptive}) {
  String? label = control.attrString("label", "")!;
  FormFieldInputBorder inputBorder = parseFormFieldInputBorder(
    control.attrString("border"),
    FormFieldInputBorder.outline,
  )!;
  var theme = Theme.of(context);
  var icon = parseIcon(control.attrString("icon"));

  var prefixIcon = parseIcon(control.attrString("prefixIcon"));
  var prefixText = control.attrString("prefixText");
  var suffixIcon = parseIcon(control.attrString("suffixIcon"));
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

  InputBorder? border;
  if (inputBorder == FormFieldInputBorder.underline) {
    border = const UnderlineInputBorder();
  } else if (inputBorder == FormFieldInputBorder.none) {
    border = InputBorder.none;
  } else if (inputBorder == FormFieldInputBorder.outline ||
      borderRadius != null ||
      borderColor != null ||
      borderWidth != null) {
    border = const OutlineInputBorder();
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
                      theme.colorScheme.onSurface.withOpacity(0.38),
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
                    theme.colorScheme.primary,
                width: focusedBorderWidth ?? borderWidth ?? 2.0));
  }

  return InputDecoration(
    enabled: !disabled,
    contentPadding: parseEdgeInsets(control, "contentPadding"),
    isDense: control.attrBool("dense"),
    label: label != "" ? Text(label) : null,
    labelStyle: parseTextStyle(theme, control, "labelStyle"),
    border: border,
    enabledBorder: border,
    focusedBorder: focusedBorder,
    hoverColor: hoverColor,
    icon: icon != null ? Icon(icon) : null,
    filled: control.attrBool("filled", false)!,
    fillColor: fillColor ?? (focused ? focusedBgcolor ?? bgcolor : bgcolor),
    hintText: control.attrString("hintText"),
    hintStyle: parseTextStyle(theme, control, "hintStyle"),
    helperText: control.attrString("helperText"),
    helperStyle: parseTextStyle(theme, control, "helperStyle"),
    counterText: control.attrString("counterText"),
    counterStyle: parseTextStyle(theme, control, "counterTextStyle"),
    counter: counter != null
        ? createControl(control, counter.id, control.isDisabled,
            parentAdaptive: adaptive)
        : null,
    helper: helper != null
        ? createControl(control, helper.id, control.isDisabled,
            parentAdaptive: adaptive)
        : null,
    error: error != null
        ? createControl(control, error.id, control.isDisabled,
            parentAdaptive: adaptive)
        : null,
    errorMaxLines: control.attrInt("errorMaxLines"),
    helperMaxLines: control.attrInt("helperMaxLines"),
    hintFadeDuration: parseDuration(control, "hintFadeDuration"),
    hintMaxLines: control.attrInt("hintMaxLines"),
    iconColor: control.attrColor("iconColor", context),
    alignLabelWithHint: control.attrBool("alignLabelWithHint", false)!,
    prefixIconColor: control.attrColor("prefixIconColor", context),
    suffixIconColor: control.attrColor("suffixIconColor", context),
    errorText: control.attrString("errorText"),
    errorStyle: parseTextStyle(theme, control, "errorTextStyle"),
    prefixIcon: prefixIcon != null ? Icon(prefixIcon) : null,
    prefixText: prefixText,
    prefixStyle: parseTextStyle(theme, control, "prefixTextStyle"),
    prefix: prefix != null
        ? createControl(control, prefix.id, control.isDisabled,
            parentAdaptive: adaptive)
        : null,
    suffix: suffix != null
        ? createControl(control, suffix.id, control.isDisabled,
            parentAdaptive: adaptive)
        : null,
    suffixIcon: suffixIcon != null ? Icon(suffixIcon) : customSuffix,
    suffixText: suffixText,
    suffixStyle: parseTextStyle(theme, control, "suffixTextStyle"),
    focusColor: control.attrColor("focusColor", context),
    floatingLabelStyle:
        parseTextStyle(theme, control, "floatingLabelTextStyle"),
  );
}

InputDecorationTheme buildInputDecorationTheme(
    BuildContext context, Control control, bool focused) {
  FormFieldInputBorder inputBorder = parseFormFieldInputBorder(
    control.attrString("border"),
    FormFieldInputBorder.outline,
  )!;
  var theme = Theme.of(context);

  var bgcolor = control.attrColor("bgcolor", context);
  var focusedBgcolor = control.attrColor("focusedBgcolor", context);
  var fillColor = control.attrColor("fillColor", context);
  var hoverColor = control.attrColor("hoverColor", context);
  var borderColor = control.attrColor("borderColor", context);

  var borderRadius = parseBorderRadius(control, "borderRadius");
  var focusedBorderColor = control.attrColor("focusedBorderColor", context);
  var borderWidth = control.attrDouble("borderWidth");
  var focusedBorderWidth = control.attrDouble("focusedBorderWidth");

  InputBorder? border;
  if (inputBorder == FormFieldInputBorder.underline) {
    border = const UnderlineInputBorder();
  } else if (inputBorder == FormFieldInputBorder.none) {
    border = InputBorder.none;
  } else if (inputBorder == FormFieldInputBorder.outline ||
      borderRadius != null ||
      borderColor != null ||
      borderWidth != null) {
    border = const OutlineInputBorder();
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
                      theme.colorScheme.onSurface.withOpacity(0.38),
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
                    theme.colorScheme.primary,
                width: focusedBorderWidth ?? borderWidth ?? 2.0));
  }

  return InputDecorationTheme(
    contentPadding: parseEdgeInsets(control, "contentPadding"),
    isDense: control.attrBool("dense", false)!,
    labelStyle: parseTextStyle(theme, control, "labelStyle"),
    border: border,
    enabledBorder: border,
    focusedBorder: focusedBorder,
    hoverColor: hoverColor,
    filled: control.attrBool("filled", false)!,
    fillColor: fillColor ?? (focused ? focusedBgcolor ?? bgcolor : bgcolor),
    hintStyle: parseTextStyle(theme, control, "hintStyle"),
    helperStyle: parseTextStyle(theme, control, "helperStyle"),
    counterStyle: parseTextStyle(theme, control, "counterTextStyle"),
    errorStyle: parseTextStyle(theme, control, "errorTextStyle"),
    prefixStyle: parseTextStyle(theme, control, "prefixTextStyle"),
    suffixStyle: parseTextStyle(theme, control, "suffixTextStyle"),
    iconColor: control.attrColor("iconColor", context),
    alignLabelWithHint: control.attrBool("alignLabelWithHint", false)!,
    prefixIconColor: control.attrColor("prefixIconColor", context),
    suffixIconColor: control.attrColor("suffixIconColor", context),
    errorMaxLines: control.attrInt("errorMaxLines"),
    helperMaxLines: control.attrInt("helperMaxLines"),
    focusColor: control.attrColor("focusColor", context),
    floatingLabelStyle:
        parseTextStyle(theme, control, "floatingLabelTextStyle"),
    activeIndicatorBorder:
        parseBorderSide(theme, control, "activeIndicatorBorderSide"),
    hintFadeDuration: parseDuration(control, "hintFadeDuration"),
  );
}

OverlayVisibilityMode parseVisibilityMode(String type) {
  switch (type.toLowerCase()) {
    case "never":
      return OverlayVisibilityMode.never;
    case "notediting":
      return OverlayVisibilityMode.notEditing;
    case "editing":
      return OverlayVisibilityMode.editing;
    case "always":
      return OverlayVisibilityMode.always;
  }
  return OverlayVisibilityMode.always;
}
