import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/text.dart';
import 'base_controls.dart';

class CupertinoDialogActionControl extends StatelessWidget {
  final Control control;

  const CupertinoDialogActionControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoDialogAction build: ${control.id}");

    var cupertinoDialogAction = CupertinoDialogAction(
      isDefaultAction: control.getBool("is_default_action", false)!,
      isDestructiveAction: control.getBool("is_destructive_action", false)!,
      textStyle: parseTextStyle(control.get("text_style"), Theme.of(context)),
      onPressed: !control.disabled
          ? () {
              FletBackend.of(context).triggerControlEvent(control, "click");
            }
          : null,
      child: control.buildWidget("content") ??
          Text(control.getString("text", "")!),
    );

    return BaseControl(control: control, child: cupertinoDialogAction);
  }
}
