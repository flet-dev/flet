import 'package:flutter/material.dart';

import '../controls/alert_dialog.dart';
import '../models/control.dart';
import '../widgets/flet_store_mixin.dart';
import 'cupertino_alert_dialog.dart';

class AdaptiveAlertDialogControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const AdaptiveAlertDialogControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("AdaptiveAlertDialog build: ${control.id}");

    return withPagePlatform((context, platform) {
      if (control.adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoAlertDialogControl(control: control);
      } else {
        return AlertDialogControl(control: control);
      }
    });
  }
}
