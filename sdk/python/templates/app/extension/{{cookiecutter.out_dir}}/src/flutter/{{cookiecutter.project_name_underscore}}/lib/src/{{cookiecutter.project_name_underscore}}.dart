import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class {{cookiecutter.control_name}}Control extends StatelessWidget {
  final Control control;

  const {{cookiecutter.control_name}}Control({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    String text = control.getString("value", "")!;
    Widget myControl = Text(text);

    return LayoutControl(control: control, child: myControl);
  }
}
