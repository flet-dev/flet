import 'package:flutter/cupertino.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import 'base_controls.dart';

class CupertinoActionSheetControl extends StatelessWidget {
  final Control control;

  const CupertinoActionSheetControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoActionSheetControl build: ${control.id}");

    var sheet = CupertinoActionSheet(
      title: control.buildTextOrWidget("title"),
      message: control.buildTextOrWidget("message"),
      cancelButton: control.buildWidget("cancel"),
      actions: control.buildWidgets("actions"),
    );

    return ConstrainedControl(control: control, child: sheet);
  }
}
