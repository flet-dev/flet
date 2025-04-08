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

    return control.buildWidget("content") ??
        const ErrorControl("RadioGroup.content must be provided and visible");
  }
}
