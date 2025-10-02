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
    dynamic value, ThemeData theme,
    [NativeTemplateTextStyle? defaultValue]) {
  if (value == null) return defaultValue;

  return NativeTemplateTextStyle(
    size: parseDouble(value["size"]),
    textColor: parseColor(value["color"], theme),
    backgroundColor: parseColor(value["bgcolor"], theme),
    style: parseNativeTemplateFontStyle(value["style"]),
  );
}

NativeTemplateStyle? parseNativeTemplateStyle(dynamic value, ThemeData theme,
    [NativeTemplateStyle? defaultValue]) {
  if (value == null) return defaultValue;

  return NativeTemplateStyle(
      templateType:
          parseTemplateType(value["template_type"], TemplateType.medium)!,
      mainBackgroundColor: parseColor(value["main_bgcolor"], theme),
      cornerRadius: parseDouble(value["corner_radius"]),
      callToActionTextStyle: parseNativeTemplateTextStyle(
          theme, value["call_to_action_text_style"]),
      primaryTextStyle:
          parseNativeTemplateTextStyle(value["primary_text_style"], theme),
      secondaryTextStyle:
          parseNativeTemplateTextStyle(value["secondary_text_style"], theme),
      tertiaryTextStyle:
          parseNativeTemplateTextStyle(value["tertiary_text_style"], theme));
}
