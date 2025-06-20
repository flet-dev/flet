import 'package:flutter/widgets.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import 'base_controls.dart';

class ControlBuilderControl extends StatelessWidget {
  final Control control;

  const ControlBuilderControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ControlBuilder.build: ${control.id}");
    return BaseControl(
        control: control,
        child: control.buildWidget("content") ?? const SizedBox.shrink());
  }
}
