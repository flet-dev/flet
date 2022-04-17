import 'package:flutter/cupertino.dart';

Alignment alignmentFromJson(Map<String, dynamic> json) {
  return Alignment(json['x'] as double, json['y'] as double);
}
