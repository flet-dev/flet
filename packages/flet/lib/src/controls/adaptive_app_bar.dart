import 'package:flutter/material.dart';

import '../models/control.dart';
import '../widgets/flet_store_mixin.dart';
import 'app_bar.dart';
import 'cupertino_app_bar.dart';

class AdaptiveAppBarControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const AdaptiveAppBarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("AdaptiveAppBarControl build: ${control.id}");

    return withPagePlatform((context, platform) {
      if (control.adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoAppBarControl(control: control);
      } else {
        return AppBarControl(control: control);
      }
    });
  }
}
