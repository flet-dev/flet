import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class CupertinoDialogActionControl extends StatelessWidget {
  final Control control;

  const CupertinoDialogActionControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoDialogAction build: ${control.id}");

    var content = control.buildTextOrWidget("content");
    if (content == null) {
      return const ErrorControl(
          "CupertinoDialogAction.content must be a string or visible Control");
    }

    var cupertinoDialogAction = CupertinoDialogAction(
      isDefaultAction: control.getBool("default", false)!,
      isDestructiveAction: control.getBool("destructive", false)!,
      textStyle: control.getTextStyle("text_style", Theme.of(context)),
      onPressed: !control.disabled ? () => control.triggerEvent("click") : null,
      child: content,
    );

    return BaseControl(control: control, child: cupertinoDialogAction);
  }
}
