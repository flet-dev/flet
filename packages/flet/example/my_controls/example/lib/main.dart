import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:my_controls/my_controls.dart' as my_controls;

void main() async {
  await setupDesktop();

  runApp(FletApp(
    pageUrl: 'http://localhost:8550',
    assetsDir: '',
    createControlFactories: [my_controls.createControl],
  ));
}
