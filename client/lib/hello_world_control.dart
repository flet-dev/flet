import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class HelloWorldControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const HelloWorldControl({Key? key, this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Text("Hello world: $control");
  }
}
