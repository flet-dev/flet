import 'package:flet/src/extensions/control.dart';
import 'package:flutter/cupertino.dart';

import '../models/control.dart';
import 'base_controls.dart';

class CupertinoActionSheetControl extends StatelessWidget {
  final Control control;

  const CupertinoActionSheetControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoActionSheetControl build: ${control.id}");

    var sheet = CupertinoActionSheet(
      title: control.buildWidget("title"),
      message: control.buildWidget("message"),
      cancelButton: control.buildWidget("cancel"),
      actions: control.buildWidgets("actions"),
    );

    return ConstrainedControl(control: control, child: sheet);
  }
}
