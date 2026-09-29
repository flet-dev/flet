import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'button.dart';
import 'card.dart';
import 'checkbox.dart';
import 'input.dart';
import 'switch.dart';
import 'theme.dart';
import 'utils/lucide_icons.dart';

/// Icon set ID of Lucide icons, see `flet_shadcn_ui.LucideIcons`.
const _lucideIconSetId = 3;

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "ShadTheme":
        return ShadThemeControl(key: key, control: control);
      case "ShadButton":
        return ShadButtonControl(key: key, control: control);
      case "ShadCard":
        return ShadCardControl(key: key, control: control);
      case "ShadInput":
        return ShadInputControl(key: key, control: control);
      case "ShadCheckbox":
        return ShadCheckboxControl(key: key, control: control);
      case "ShadSwitch":
        return ShadSwitchControl(key: key, control: control);
      default:
        return null;
    }
  }

  @override
  IconData? createIconData(int iconCode) {
    if ((iconCode >> 16) & 0xFF != _lucideIconSetId) return null;
    final index = iconCode & 0xFFFF;
    return index < lucideIcons.length ? lucideIcons[index] : null;
  }
}
