import 'package:flutter/material.dart';

import '../models/control.dart';
import '../widgets/flet_store_mixin.dart';
import 'cupertino_switch.dart';
import 'switch.dart';

class AdaptiveSwitchControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const AdaptiveSwitchControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("AdaptiveSwitch build: ${control.id}");

    return withPagePlatform((context, platform) {
      if (control.adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoSwitchControl(control: control);
      } else {
        return SwitchControl(control: control);
      }
    });
  }
}
