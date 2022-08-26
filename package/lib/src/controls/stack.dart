import 'package:flutter/widgets.dart';

import '../models/control.dart';
import 'create_control.dart';

class StackControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;

  const StackControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Stack build: ${control.id}");

    var clipBehavior = Clip.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("clipBehavior", "")!.toLowerCase(),
        orElse: () => Clip.hardEdge);

    bool disabled = control.isDisabled || parentDisabled;

    return constrainedControl(
        Stack(
          clipBehavior: clipBehavior,
          children: children
              .where((c) => c.isVisible)
              .map((c) => createControl(control, c.id, disabled))
              .toList(),
        ),
        parent,
        control);
  }
}
