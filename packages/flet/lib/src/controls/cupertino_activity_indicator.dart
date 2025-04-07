import 'package:flet/src/utils/colors.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/cupertino.dart';

import '../models/control.dart';
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
    final activityIndicator = CupertinoActivityIndicator(
      radius: control.getDouble("radius", 10)!,
      animating: control.getBool("animating", true)!,
      color: control.getColor("color", context),
    );
    return ConstrainedControl(control: control, child: activityIndicator);
  }
}
