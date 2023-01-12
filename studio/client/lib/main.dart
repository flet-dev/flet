import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

void main() async {
  await setupDesktop();
  runApp(const FletApp(
    pageUrl: "http://192.168.1.243:8550/",
    assetsDir: "",
  ));
}
