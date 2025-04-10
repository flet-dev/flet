import 'package:flutter/widgets.dart';

import '../models/control.dart';
import 'control_widget.dart';

class CenterControl extends StatelessWidget {
  final Control control;

  const CenterControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Center.build: ${control.id}");

    Widget child = SizedBox.shrink();
    var value = control.properties["child"];
    if (value is Control) {
      child = ControlWidget(control: value);
    }
    return Center(child: child);
  }
}
