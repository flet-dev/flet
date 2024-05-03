import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../controls/create_control.dart';
import '../models/control.dart';
import 'borders.dart';
import 'edge_insets.dart';
import 'icons.dart';
import 'text.dart';

enum FormFieldInputBorder { outline, underline, none }

TextInputType parseTextInputType(String type) {
  switch (type.toLowerCase()) {
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
  }
  return TextInputType.text;
}

InputDecoration buildInputDecoration(
    BuildContext context,
    Control control,
    Control? prefix,
    Control? suffix,
    Widget? customSuffix,
    bool focused,
    bool disabled,
    bool? adaptive) {
  String? label = control.attrString("label", "")!;
  FormFieldInputBorder inputBorder = FormFieldInputBorder.values.firstWhere(
    ((b) => b.name == control.attrString("border", "")!.toLowerCase()),
    orElse: () => FormFieldInputBorder.outline,
  );
  var icon = parseIcon(control.attrString("icon", "")!);

  var prefixIcon = parseIcon(control.attrString("prefixIcon", "")!);
  var prefixText = control.attrString("prefixText");
  var suffixIcon = parseIcon(control.attrString("suffixIcon", "")!);
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
      label: label != "" ? Text(label) : null,
      labelStyle: parseTextStyle(Theme.of(context), control, "labelStyle"),
      border: border,
      enabledBorder: border,
      focusedBorder: focusedBorder,
      hoverColor: hoverColor,
      icon: icon != null ? Icon(icon) : null,
      filled: control.attrBool("filled", false)!,
      fillColor: fillColor ?? (focused ? focusedBgcolor ?? bgcolor : bgcolor),
      hintText: control.attrString("hintText"),
      hintStyle: parseTextStyle(Theme.of(context), control, "hintStyle"),
      helperText: control.attrString("helperText"),
      helperStyle: parseTextStyle(Theme.of(context), control, "helperStyle"),
      counterText: control.attrString("counterText"),
      counterStyle: parseTextStyle(Theme.of(context), control, "counterStyle"),
      errorText: control.attrString("errorText"),
      errorStyle: parseTextStyle(Theme.of(context), control, "errorStyle"),
      prefixIcon: prefixIcon != null ? Icon(prefixIcon) : null,
      prefixText: prefixText,
      prefixStyle: parseTextStyle(Theme.of(context), control, "prefixStyle"),
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
      suffixStyle: parseTextStyle(Theme.of(context), control, "suffixStyle"));
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
