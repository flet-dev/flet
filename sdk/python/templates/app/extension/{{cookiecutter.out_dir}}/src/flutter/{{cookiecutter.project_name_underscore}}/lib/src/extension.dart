import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import '{{cookiecutter.project_name_underscore}}.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "{{cookiecutter.control_name}}":
        return {{cookiecutter.control_name}}Control(control: control);
      default:
        return null;
    }
  }
}
