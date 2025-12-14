import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/keys.dart';
import '../widgets/control_wrappers.dart';
import '../widgets/error.dart';

class ControlWidget extends StatelessWidget {
  final Control control;

  const ControlWidget({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    ControlKey? controlKey = control.getKey("key");
    Key? key;
    if (controlKey is ControlScrollKey) {
      key = GlobalKey();
      FletBackend.of(context).globalKeys[controlKey.toString()] =
          key as GlobalKey;
    } else if (controlKey != null) {
      key = ValueKey(controlKey.value);
    }

    Widget? widget;
    if (control.internals?["skip_inherited_notifier"] == true) {
      for (var extension in FletBackend.of(context).extensions) {
        widget = extension.createWidget(key, control);
        if (widget != null) return widget;
      }
      widget = ErrorControl("Unknown control: ${control.type}");
    } else {
      widget = withControlInheritedNotifier(control, (context) {
        Widget? cw;
        for (var extension in FletBackend.of(context).extensions) {
          cw = extension.createWidget(key, control);
          if (cw != null) return cw;
        }

        return ErrorControl("Unknown control: ${control.type}");
      });
    }

    final isRootControl = control == FletBackend.of(context).page;
    return wrapWithControlTheme(control, context, widget,
        isRootControl: isRootControl);
  }
}
