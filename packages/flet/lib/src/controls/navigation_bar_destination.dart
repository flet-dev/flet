import 'package:flet/src/utils/icons.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class NavigationBarDestinationControl extends StatelessWidget {
  final Control control;

  const NavigationBarDestinationControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("NavigationBarDestination build: ${control.id}");

    var icon = parseIcon(control.getString("icon"));
    var selectedIcon = parseIcon(control.getString("selected_icon"));
    var child = NavigationDestination(
        enabled: !control.disabled,
        tooltip: !control.disabled ? control.getString("tooltip") : null,
        icon: control.buildWidget("icon") ?? Icon(icon),
        selectedIcon: control.buildWidget("selected_icon") ??
            (selectedIcon != null ? Icon(selectedIcon) : null),
        label: control.getString("label", "")!);

    return BaseControl(control: control, child: child);
  }
}
