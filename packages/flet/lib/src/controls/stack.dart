import 'package:flutter/widgets.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
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
      clipBehavior: control.getClipBehavior("clip_behavior", Clip.hardEdge)!,
      fit: control.getStackFit("fit", StackFit.loose)!,
      alignment:
          control.getAlignment("alignment") ?? AlignmentDirectional.topStart,
      children: control.buildWidgets("controls"),
    );
    return LayoutControl(control: control, child: stack);
  }
}
