import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'auto_suggest_box.dart';
import 'breadcrumb_bar.dart';
import 'button.dart';
import 'calendar.dart';
import 'card.dart';
import 'color_picker.dart';
import 'command_bar.dart';
import 'combo_box.dart';
import 'content_dialog.dart';
import 'date_picker.dart';
import 'divider.dart';
import 'dropdown_button.dart';
import 'expander.dart';
import 'flyout.dart';
import 'info_badge.dart';
import 'info_bar.dart';
import 'info_label.dart';
import 'list_tile.dart';
import 'menu_bar.dart';
import 'navigation_view.dart';
import 'number_box.dart';
import 'password_box.dart';
import 'progress.dart';
import 'radio_group.dart';
import 'rating_bar.dart';
import 'slider.dart';
import 'tab_view.dart';
import 'text_box.dart';
import 'theme.dart';
import 'toggles.dart';
import 'tooltip.dart';
import 'tree_view.dart';
import 'utils/fluent_icons.dart';
import 'utils/theme.dart';

/// Icon set ID of Fluent icons, see `flet_fluent_ui.FluentIcons`.
const _fluentIconSetId = 4;

class Extension extends FletExtension {
  @override
  Widget wrapApp(BuildContext context, Widget child) =>
      wrapAppWithFluentTheme(context, child);

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
      case "FluentDatePicker":
        return FluentDatePickerControl(key: key, control: control);
      case "FluentTimePicker":
        return FluentTimePickerControl(key: key, control: control);
      case "FluentCalendarView":
        return FluentCalendarControl(key: key, control: control);
      case "FluentCalendarDatePicker":
        return FluentCalendarControl(key: key, control: control, picker: true);
      case "FluentColorPicker":
        return FluentColorPickerControl(key: key, control: control);
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
      case "FluentEditableComboBox":
        return FluentEditableComboBoxControl(key: key, control: control);
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
      case "FluentPasswordBox":
        return FluentPasswordBoxControl(key: key, control: control);
      case "FluentNumberBox":
        return FluentNumberBoxControl(key: key, control: control);
      case "FluentAutoSuggestBox":
        return FluentAutoSuggestBoxControl(key: key, control: control);
      case "FluentInfoLabel":
        return FluentInfoLabelControl(key: key, control: control);
      case "FluentRatingBar":
        return FluentRatingBarControl(key: key, control: control);
      case "FluentDivider":
        return FluentDividerControl(key: key, control: control);
      case "FluentListTile":
        return FluentListTileControl(key: key, control: control);
      case "FluentInfoBadge":
        return FluentInfoBadgeControl(key: key, control: control);
      case "FluentFlyout":
        return FluentFlyoutControl(key: key, control: control);
      case "FluentTeachingTip":
        return FluentFlyoutControl(
          key: key,
          control: control,
          teachingTip: true,
        );
      case "FluentContextMenu":
        return FluentContextMenuControl(key: key, control: control);
      case "FluentDropDownButton":
        return FluentDropDownButtonControl(key: key, control: control);
      case "FluentSplitButton":
        return FluentSplitButtonControl(key: key, control: control);
      case "FluentMenuBar":
        return FluentMenuBarControl(key: key, control: control);
      case "FluentCommandBar":
        return FluentCommandBarControl(key: key, control: control);
      case "FluentTabView":
        return FluentTabViewControl(key: key, control: control);
      case "FluentTreeView":
        return FluentTreeViewControl(key: key, control: control);
      case "FluentBreadcrumbBar":
        return FluentBreadcrumbBarControl(key: key, control: control);
      case "FluentNavigationView":
        return FluentNavigationViewControl(key: key, control: control);
      case "FluentScaffoldPage":
        return FluentScaffoldPageControl(key: key, control: control);
      case "FluentPageHeader":
        return FluentPageHeaderControl(key: key, control: control);
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
