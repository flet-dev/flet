import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../widgets/error.dart';

class RadioGroupControl extends StatelessWidget {
  final Control control;

  const RadioGroupControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("RadioGroupControl build: ${control.id}");

    return RadioGroup<String>(
      groupValue: control.get<String>("value"),
      onChanged: (String? value) {
        if (!control.disabled) {
          control.updateProperties({"value": value}, notify: true);
          control.triggerEvent("change", value);
        }
      },
      child: control.buildWidget("content") ??
          const ErrorControl("RadioGroup.content must be provided and visible"),
    );
  }
}
