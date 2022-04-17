import 'package:flutter/cupertino.dart';

EdgeInsets edgeInsetsFromJson(Map<String, dynamic> json) {
  return EdgeInsets.fromLTRB(json['l'] as double, json['t'] as double,
      json['r'] as double, json['b'] as double);
}
