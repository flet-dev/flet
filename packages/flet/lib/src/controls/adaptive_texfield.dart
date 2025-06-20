import 'package:flutter/material.dart';

import '../models/control.dart';
import '../widgets/flet_store_mixin.dart';
import 'cupertino_textfield.dart';
import 'textfield.dart';

class AdaptiveTextFieldControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const AdaptiveTextFieldControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("AdaptiveTextFieldControl build: ${control.id}");

    return withPagePlatform((context, platform) {
      if (control.adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoTextFieldControl(control: control);
      } else {
        return TextFieldControl(control: control);
      }
    });
  }
}
