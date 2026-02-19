import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'code_editor.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "CodeEditor":
        return CodeEditorControl(control: control);
      default:
        return null;
    }
  }
}
