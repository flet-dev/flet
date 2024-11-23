import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

TemplateType? parseTemplateType(String? value, [TemplateType? defaultValue]) {
  if (value == null) return defaultValue;
  return TemplateType.values.firstWhereOrNull(
          (e) => e.toString().toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

NativeTemplateFontStyle? parseNativeTemplateFontStyle(String? value,
    [NativeTemplateFontStyle? defaultValue]) {
  if (value == null) return defaultValue;
  return NativeTemplateFontStyle.values.firstWhereOrNull(
          (e) => e.toString().toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

NativeTemplateTextStyle? parseNativeTemplateTextStyle(
    ThemeData theme, Control control, String propName) {
  dynamic j;
  var v = control.attrString(propName, null);
  if (v == null) return null;

  j = json.decode(v);
  return nativeTextStyleFromJson(theme, j);
}

NativeTemplateTextStyle? nativeTextStyleFromJson(
    ThemeData theme, Map<String, dynamic>? json) {
  if (json == null) return null;
  return NativeTemplateTextStyle(
    size: parseDouble(json["size"]),
    textColor: parseColor(theme, json["color"]),
    backgroundColor: parseColor(theme, json["bgColor"]),
    style: parseNativeTemplateFontStyle(json["style"]),
  );
}

NativeTemplateStyle? parseNativeTemplateStyle(
    ThemeData theme, Control control, String propName) {
  dynamic j;
  var v = control.attrString(propName, null);
  if (v == null) return null;

  j = json.decode(v);
  return nativeTemplateStyleFromJson(theme, j);
}

NativeTemplateStyle nativeTemplateStyleFromJson(
    ThemeData theme, Map<String, dynamic> json) {
  return NativeTemplateStyle(
      templateType:
          parseTemplateType(json["template_type"], TemplateType.medium)!,
      mainBackgroundColor: parseColor(theme, "main_bgcolor"),
      cornerRadius: parseDouble(json["corner_radius"]),
      callToActionTextStyle:
          nativeTextStyleFromJson(theme, json["call_to_action_text_style"]),
      primaryTextStyle:
          nativeTextStyleFromJson(theme, json["primary_text_style"]),
      secondaryTextStyle:
          nativeTextStyleFromJson(theme, json["secondary_text_style"]),
      tertiaryTextStyle:
          nativeTextStyleFromJson(theme, json["tertiary_text_style"]));
}
