import 'package:flutter/widgets.dart';
import '../models/control.dart';
import 'create_control.dart';

class ListViewControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;

  const ListViewControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("ListViewControl build: ${control.id}");

    bool disabled = control.isDisabled || parentDisabled;

    final horizontal = control.attrBool("horizontal", false)!;
    final spacing = control.attrDouble("spacing", 0)!;
    final padding = parseEdgeInsets(control, "padding");

    List<Widget> controls = [];

    bool firstControl = true;
    for (var ctrl in children.where((c) => c.isVisible)) {
      // spacer between displayed controls
      if (spacing > 0 && !firstControl) {
        controls.add(
            horizontal ? SizedBox(width: spacing) : SizedBox(height: spacing));
      }
      firstControl = false;

      // displayed control
      controls.add(createControl(control, ctrl.id, disabled));
    }

    return constrainedControl(
        ListView(
          scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
          padding: padding,
          children: controls,
        ),
        parent,
        control);
  }
}
