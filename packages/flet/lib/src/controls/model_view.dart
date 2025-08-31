import 'package:flutter/widgets.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import 'base_controls.dart';

class ModelViewControl extends StatelessWidget {
  final Control control;

  const ModelViewControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ModelView.build: ${control.id}");
    return BaseControl(
        control: control,
        child: control.buildWidget("_content") ?? const SizedBox.shrink());
  }
}
