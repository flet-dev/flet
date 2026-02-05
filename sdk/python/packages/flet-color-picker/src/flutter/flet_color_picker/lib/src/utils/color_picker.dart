import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

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
