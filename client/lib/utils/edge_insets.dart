import 'package:flutter/cupertino.dart';

EdgeInsets edgeInsetsFromJson(Map<String, dynamic> json) {
  return EdgeInsets.fromLTRB(json['left'] as double, json['top'] as double,
      json['right'] as double, json['bottom'] as double);
}
