import 'package:flutter/widgets.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import 'create_control.dart';

class StackControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final List<Control> children;

  const StackControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("Stack build: ${control.id}");
    bool disabled = control.isDisabled || parentDisabled;
    bool? adaptive = control.attrBool("adaptive") ?? parentAdaptive;

    var clipBehavior = Clip.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("clipBehavior", "")!.toLowerCase(),
        orElse: () => Clip.hardEdge);

    StackFit fit = StackFit.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("fit", "")!.toLowerCase(),
        orElse: () => StackFit.loose);
    var ctrls = children
        .where((c) => c.isVisible)
        .map((c) =>
            createControl(control, c.id, disabled, parentAdaptive: adaptive))
        .toList();

    return constrainedControl(
        context,
        Stack(
          clipBehavior: clipBehavior,
          fit: fit,
          alignment: parseAlignment(control, "alignment") ??
              AlignmentDirectional.topStart,
          children: ctrls,
        ),
        parent,
        control);
  }
}
