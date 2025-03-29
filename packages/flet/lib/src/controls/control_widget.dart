import 'package:flutter/widgets.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../widgets/control_inherited_notifier.dart';
import '../widgets/error.dart';

class ControlWidget extends StatelessWidget {
  final Control control;
  const ControlWidget({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    if (control.type == "LineChart") {
      for (var extension in FletBackend.of(context).extensions) {
        var cw = extension.createWidget(control);
        if (cw != null) return cw;
      }
      return ErrorControl("Unknown control: ${control.type}");
    } else {
      return ControlInheritedNotifier(
        notifier: control,
        child: Builder(builder: (context) {
          ControlInheritedNotifier.of(context);

          Widget? cw;
          for (var extension in FletBackend.of(context).extensions) {
            cw = extension.createWidget(control);
            if (cw != null) return cw;
          }

          return ErrorControl("Unknown control: ${control.type}");
        }),
      );
    }
  }
}
