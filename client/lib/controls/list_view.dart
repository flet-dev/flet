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

    return commonControl(
        ListView(
          scrollDirection: control.attrBool("horizontal", false)!
              ? Axis.horizontal
              : Axis.vertical,
          children: children
              .where((c) => c.isVisible)
              .map((c) => createControl(control, c.id, disabled))
              .toList(),
        ),
        parent,
        control);
  }
}
