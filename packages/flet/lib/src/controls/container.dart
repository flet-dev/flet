import 'package:flutter/material.dart';

import '../models/control.dart';
import 'control_widget.dart';

class ContainerControl extends StatelessWidget {
  final Control control;
  const ContainerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Container.build: ${control.id}");
    double paddingValue =
        (control.properties["padding"] as num?)?.toDouble() ?? 0;
    Widget child = SizedBox.shrink();
    var value = control.properties["child"];
    if (value is Control) {
      child = ControlWidget(control: value);
    }
    return Container(
      padding: EdgeInsets.all(paddingValue),
      child: child,
    );
  }
}
