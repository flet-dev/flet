import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

void main() async {
  await setupDesktop();
  runApp(const FletApp(
    pageUrl: "http://Feodors-MacBook-Pro.local:8550",
    assetsDir: "",
  ));
}
