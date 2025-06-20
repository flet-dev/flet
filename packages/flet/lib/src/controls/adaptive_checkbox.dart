import 'package:flutter/material.dart';

import '../models/control.dart';
import '../widgets/flet_store_mixin.dart';
import 'checkbox.dart';
import 'cupertino_checkbox.dart';

class AdaptiveCheckboxControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const AdaptiveCheckboxControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("AdaptiveCheckboxControl build: ${control.id}");

    return withPagePlatform((context, platform) {
      if (control.adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoCheckboxControl(control: control);
      } else {
        return CheckboxControl(control: control);
      }
    });
  }
}
