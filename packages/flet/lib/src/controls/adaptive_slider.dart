import 'package:flutter/material.dart';

import '../models/control.dart';
import '../widgets/flet_store_mixin.dart';
import 'cupertino_slider.dart';
import 'slider.dart';

class AdaptiveSliderControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const AdaptiveSliderControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("AdaptiveSlider build: ${control.id}");

    return withPagePlatform((context, platform) {
      if (control.adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoSliderControl(control: control);
      } else {
        return SliderControl(control: control);
      }
    });
  }
}
