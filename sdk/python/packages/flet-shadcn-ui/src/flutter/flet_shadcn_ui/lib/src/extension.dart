import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'alert.dart';
import 'avatar.dart';
import 'badge.dart';
import 'breadcrumb.dart';
import 'button.dart';
import 'card.dart';
import 'checkbox.dart';
import 'icon_button.dart';
import 'input.dart';
import 'input_otp.dart';
import 'progress.dart';
import 'radio_group.dart';
import 'select.dart';
import 'separator.dart';
import 'slider.dart';
import 'switch.dart';
import 'tabs.dart';
import 'textarea.dart';
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
      case "ShadAlert":
        return ShadAlertControl(key: key, control: control);
      case "ShadAvatar":
        return ShadAvatarControl(key: key, control: control);
      case "ShadBadge":
        return ShadBadgeControl(key: key, control: control);
      case "ShadBreadcrumb":
        return ShadBreadcrumbControl(key: key, control: control);
      case "ShadBreadcrumbItem":
        return ShadBreadcrumbItemControl(key: key, control: control);
      case "ShadBreadcrumbEllipsis":
        return const ShadBreadcrumbEllipsisControl();
      case "ShadButton":
        return ShadButtonControl(key: key, control: control);
      case "ShadCard":
        return ShadCardControl(key: key, control: control);
      case "ShadIconButton":
        return ShadIconButtonControl(key: key, control: control);
      case "ShadInput":
        return ShadInputControl(key: key, control: control);
      case "ShadCheckbox":
        return ShadCheckboxControl(key: key, control: control);
      case "ShadInputOTP":
        return ShadInputOTPControl(key: key, control: control);
      case "ShadProgress":
        return ShadProgressControl(key: key, control: control);
      case "ShadRadioGroup":
        return ShadRadioGroupControl(key: key, control: control);
      case "ShadRadio":
        return ShadRadioControl(key: key, control: control);
      case "ShadSelect":
        return ShadSelectControl(key: key, control: control);
      case "ShadSeparator":
        return ShadSeparatorControl(key: key, control: control);
      case "ShadSlider":
        return ShadSliderControl(key: key, control: control);
      case "ShadSwitch":
        return ShadSwitchControl(key: key, control: control);
      case "ShadTabs":
        return ShadTabsControl(key: key, control: control);
      case "ShadTextarea":
        return ShadTextareaControl(key: key, control: control);
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
