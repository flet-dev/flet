import 'package:flutter/widgets.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import 'base_controls.dart';

class CenterControl extends StatelessWidget {
  final Control control;

  const CenterControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Center.build: ${control.id}");
    return BaseControl(
        control: control, child: Center(child: control.buildWidget("content")));
  }
}
