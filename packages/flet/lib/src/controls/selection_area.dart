import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class SelectionAreaControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const SelectionAreaControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("SelectionArea build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    if (contentCtrls.isEmpty) {
      return const ErrorControl(
          "SelectionArea.content must be provided and visible");
    }
    bool disabled = control.isDisabled || parentDisabled;
    var selectionArea = SelectionArea(
      child: createControl(control, contentCtrls.first.id, disabled,
          parentAdaptive: parentAdaptive),
      onSelectionChanged: (SelectedContent? selection) {
        backend.triggerControlEvent(control.id, "change", selection?.plainText);
      },
    );

    return baseControl(context, selectionArea, parent, control);
  }
}
