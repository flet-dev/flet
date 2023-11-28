import 'package:flutter/material.dart';
import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class SelectionAreaControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const SelectionAreaControl(
      {Key? key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("SelectionArea build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    if (contentCtrls.isEmpty) {
      return const ErrorControl(
          "Content control must be specified and be visible.");
    }
    bool disabled = control.isDisabled || parentDisabled;

    Widget child = createControl(control, contentCtrls.first.id, disabled);

    return baseControl(
        context,
        SelectionArea(
          child: child,
        ),
        parent,
        control);
  }
}
