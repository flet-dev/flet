import 'package:flutter/widgets.dart';
import '../models/control.dart';
import 'create_control.dart';

class ColumnControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;

  const ColumnControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Column build: ${control.id}");

    bool disabled = control.isDisabled || parentDisabled;

    return expandable(
        Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: control.childIds
              .map((childId) => createControl(control, childId, disabled))
              .toList(),
        ),
        control);
  }
}
