import 'package:flutter/material.dart';

import '../models/control.dart';
import '../widgets/flet_store_mixin.dart';
import 'cupertino_radio.dart';
import 'radio.dart';

class AdaptiveRadioControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const AdaptiveRadioControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("AdaptiveRadioControl build: ${control.id}");

    return withPagePlatform((context, platform) {
      if (control.adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoRadioControl(control: control);
      } else {
        return RadioControl(control: control);
      }
    });
  }
}
