import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class RadioGroupControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const RadioGroupControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("RadioGroupControl build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    if (contentCtrls.isEmpty) {
      return const ErrorControl(
          "RadioGroup control does not have any content.");
    }

    return createControl(control, contentCtrls.first.id, disabled);
  }
}
