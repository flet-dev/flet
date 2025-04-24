import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class SelectionAreaControl extends StatelessWidget {
  final Control control;

  const SelectionAreaControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("SelectionArea build: ${control.id}");

    var content = control.buildWidget("content");
    if (content == null) {
      return const ErrorControl(
          "SelectionArea.content must be provided and visible");
    }
    var selectionArea = SelectionArea(
      child: content,
      onSelectionChanged: (SelectedContent? selection) {
        control.triggerEvent("change", data: selection?.plainText);
      },
    );

    return BaseControl(control: control, child: selectionArea);
  }
}
