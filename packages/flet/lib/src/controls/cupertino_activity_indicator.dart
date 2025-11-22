import 'package:flutter/cupertino.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class CupertinoActivityIndicatorControl extends StatelessWidget {
  final Control control;

  const CupertinoActivityIndicatorControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoActivityIndicatorControl build: ${control.id}");
    final radius = control.getDouble("radius", 10)!;
    final color = control.getColor("color", context);
    final progress = control.getDouble("progress");
    final bool animating =
        progress == null ? control.getBool("animating", true)! : false;

    final activityIndicator = progress != null
        ? CupertinoActivityIndicator.partiallyRevealed(
            radius: radius,
            color: color,
            progress: progress,
          )
        : CupertinoActivityIndicator(
            radius: radius,
            animating: animating,
            color: color,
          );
    return LayoutControl(control: control, child: activityIndicator);
  }
}
