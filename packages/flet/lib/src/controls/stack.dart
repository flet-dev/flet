import 'package:flutter/widgets.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/misc.dart';
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
    final stack = Stack(
      clipBehavior:
          parseClip(control.getString("clipBehavior"), Clip.hardEdge)!,
      fit: parseStackFit(control.getString("fit"), StackFit.loose)!,
      alignment:
          control.getAlignment("alignment") ?? AlignmentDirectional.topStart,
      children: control.buildWidgets("controls"),
    );
    return ConstrainedControl(control: control, child: stack);
  }
}
