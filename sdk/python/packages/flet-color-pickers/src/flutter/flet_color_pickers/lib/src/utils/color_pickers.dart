import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

HSVColor? parseHsvColor(dynamic value) {
  if (value is Map) {
    final alpha = parseDouble(value["alpha"]);
    final hue = parseDouble(value["hue"]);
    final saturation = parseDouble(value["saturation"]);
    final val = parseDouble(value["value"]);
    if (alpha != null && hue != null && saturation != null && val != null) {
      return HSVColor.fromAHSV(alpha, hue, saturation, val);
    }
  }
  return null;
}

PaletteType? parsePaletteType(String? value, [PaletteType? defaultValue]) {
  return parseEnum(PaletteType.values, value, defaultValue);
}

ColorLabelType? parseLabelType(String? value, [ColorLabelType? defaultValue]) {
  return parseEnum(ColorLabelType.values, value, defaultValue);
}

ColorModel? parseColorModel(String? value, [ColorModel? defaultValue]) {
  return parseEnum(ColorModel.values, value, defaultValue);
}
