import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'button.dart';
import 'card.dart';
import 'combo_box.dart';
import 'content_dialog.dart';
import 'expander.dart';
import 'info_bar.dart';
import 'progress.dart';
import 'radio_group.dart';
import 'slider.dart';
import 'text_box.dart';
import 'theme.dart';
import 'toggles.dart';
import 'tooltip.dart';
import 'utils/fluent_icons.dart';

/// Icon set ID of Fluent icons, see `flet_fluent_ui.FluentIcons`.
const _fluentIconSetId = 4;

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    final widget = _createWidget(key, control);
    if (widget != null) {
      // Fluent controls draw FluentIcons glyphs (checkmarks, chevrons, info
      // bar icons): a web build loads that font on first use.
      loadDeferredFonts("fluent_ui");
    }
    return widget;
  }

  Widget? _createWidget(Key? key, Control control) {
    switch (control.type) {
      case "FluentTheme":
        return FluentThemeControl(key: key, control: control);
      case "FluentButton":
      case "FluentFilledButton":
      case "FluentOutlinedButton":
      case "FluentHyperlinkButton":
      case "FluentIconButton":
        return FluentButtonControl(key: key, control: control);
      case "FluentToggleButton":
        return FluentToggleButtonControl(key: key, control: control);
      case "FluentCheckbox":
        return FluentCheckboxControl(key: key, control: control);
      case "FluentToggleSwitch":
        return FluentToggleSwitchControl(key: key, control: control);
      case "FluentRadioGroup":
        return FluentRadioGroupControl(key: key, control: control);
      case "FluentRadioButton":
        return FluentRadioButtonControl(key: key, control: control);
      case "FluentSlider":
        return FluentSliderControl(key: key, control: control);
      case "FluentTextBox":
        return FluentTextBoxControl(key: key, control: control);
      case "FluentComboBox":
        return FluentComboBoxControl(key: key, control: control);
      case "FluentProgressBar":
        return FluentProgressControl(key: key, control: control, ring: false);
      case "FluentProgressRing":
        return FluentProgressControl(key: key, control: control, ring: true);
      case "FluentInfoBar":
        return FluentInfoBarControl(key: key, control: control);
      case "FluentExpander":
        return FluentExpanderControl(key: key, control: control);
      case "FluentCard":
        return FluentCardControl(key: key, control: control);
      case "FluentTooltip":
        return FluentTooltipControl(key: key, control: control);
      case "FluentContentDialog":
        return FluentContentDialogControl(key: key, control: control);
      default:
        return null;
    }
  }

  @override
  IconData? createIconData(int iconCode) {
    if ((iconCode >> 16) & 0xFF != _fluentIconSetId) return null;
    final index = iconCode & 0xFFFF;
    if (index >= fluentIcons.length) return null;
    loadDeferredFonts("fluent_ui");
    return fluentIcons[index];
  }
}
