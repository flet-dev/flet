import 'package:flutter/widgets.dart';

import '../models/control.dart';
import 'control_widget.dart';

class RowControl extends StatelessWidget {
  final Control control;
  const RowControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Row.build: ${control.id}");

    MainAxisAlignment mainAxisAlignment = MainAxisAlignment.start;
    if (control.properties.containsKey("mainAxisAlignment")) {
      String alignStr = control.properties["mainAxisAlignment"];
      if (alignStr == "center") {
        mainAxisAlignment = MainAxisAlignment.center;
      } else if (alignStr == "end") {
        mainAxisAlignment = MainAxisAlignment.end;
      }
    }

    return Row(
      mainAxisAlignment: mainAxisAlignment,
      spacing: control.getDouble("spacing", 10)!,
      children: control
          .children("controls")
          .map(
              (child) => ControlWidget(control: child, key: ValueKey(child.id)))
          .toList(),
    );
  }
}
