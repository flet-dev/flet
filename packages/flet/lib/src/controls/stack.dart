import 'package:flutter/widgets.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/others.dart';
import 'base_controls.dart';

class StackControl extends StatelessWidget {
  final Control control;

  const StackControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("Stack build: ${control.id}");
    var clipBehavior =
        parseClip(control.getString("clipBehavior"), Clip.hardEdge)!;
    var fit = parseStackFit(control.getString("fit"), StackFit.loose)!;
    var controls = control.buildWidgets("controls");

    return ConstrainedControl(
        control: control,
        child: Stack(
          clipBehavior: clipBehavior,
          fit: fit,
          alignment: parseAlignment(control, "alignment") ??
              AlignmentDirectional.topStart,
          children: controls,
        ));
  }
}
