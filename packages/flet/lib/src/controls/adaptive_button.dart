import 'package:flutter/material.dart';

import '../models/control.dart';
import '../widgets/flet_store_mixin.dart';
import 'button.dart';
import 'cupertino_button.dart';
import 'cupertino_dialog_action.dart';

class AdaptiveButtonControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const AdaptiveButtonControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("AdaptiveElevatedButton build: ${control.id}");

    return withPagePlatform((context, platform) {
      if (control.adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return (control.parent?.type == "AlertDialog" ||
                control.parent?.type == "CupertinoAlertDialog")
            ? CupertinoDialogActionControl(
                control: control,
              )
            : CupertinoButtonControl(
                control: control,
              );
      } else {
        return ButtonControl(control: control);
      }
    });
  }
}
