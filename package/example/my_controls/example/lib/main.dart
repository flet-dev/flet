import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:my_controls/my_controls.dart' as my_controls;

var factories = [my_controls.createControl];

void main() {
  runApp(const FletApp(
    pageUrl: 'http://localhost:8550',
    assetsDir: '',
  ));
}
