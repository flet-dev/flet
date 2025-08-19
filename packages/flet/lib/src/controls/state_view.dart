import 'package:flutter/widgets.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import 'base_controls.dart';

class StateViewControl extends StatelessWidget {
  final Control control;

  const StateViewControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("StateView.build: ${control.id}");
    return BaseControl(
        control: control,
        child: control.buildWidget("content") ?? const SizedBox.shrink());
  }
}
