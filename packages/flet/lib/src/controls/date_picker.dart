import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/icons.dart';
import '../utils/locale.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';

class DatePickerControl extends StatelessWidget {
  final Control control;

  const DatePickerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("DatePicker build: ${control.id}");

    bool lastOpen = control.getBool("_open", false)!;

    var open = control.getBool("open", false)!;
    var value = control.getDateTime("value");
    var currentDate = control.getDateTime("current_date");
    var switchToCalendarEntryModeIcon =
        control.getIconData("switch_to_calendar_icon");
    var switchToInputEntryModeIcon =
        control.getIconData("switch_to_input_icon");
    var locale = control.getLocale("locale");

    void onClosed(DateTime? dateValue) {
      control.updateProperties({"_open": false}, python: false);
      control.updateProperties({"value": dateValue ?? value, "open": false});
      if (dateValue != null) {
        control.triggerEvent("change", dateValue);
      }
      control.triggerEvent("dismiss", dateValue == null);
    }

    Widget createSelectDateDialog() {
      Widget dialog = DatePickerDialog(
        initialDate: value ?? currentDate ?? DateTime.now(),
        firstDate: control.getDateTime("first_date", DateTime(1900, 1, 1))!,
        lastDate: control.getDateTime("last_date", DateTime(2050, 1, 1))!,
        currentDate: currentDate ?? DateTime.now(),
        helpText: control.getString("help_text"),
        cancelText: control.getString("cancel_text"),
        confirmText: control.getString("confirm_text"),
        errorFormatText: control.getString("error_format_text"),
        errorInvalidText: control.getString("error_invalid_text"),
        keyboardType: parseTextInputType(
            control.getString("keyboard_type"), TextInputType.text)!,
        initialCalendarMode:
            control.getDatePickerMode("date_picker_mode", DatePickerMode.day)!,
        initialEntryMode: control.getDatePickerEntryMode(
            "entry_mode", DatePickerEntryMode.calendar)!,
        fieldHintText: control.getString("field_hint_text"),
        fieldLabelText: control.getString("field_label_text"),
        insetPadding: control.getPadding("inset_padding",
            const EdgeInsets.symmetric(horizontal: 16.0, vertical: 24.0))!,
        onDatePickerModeChange: (DatePickerEntryMode mode) {
          control.updateProperties({"entry_mode": mode.name});
          control.triggerEvent("entry_mode_change", {"entry_mode": mode.name});
        },
        switchToCalendarEntryModeIcon: switchToCalendarEntryModeIcon != null
            ? Icon(switchToCalendarEntryModeIcon)
            : null,
        switchToInputEntryModeIcon: switchToInputEntryModeIcon != null
            ? Icon(switchToInputEntryModeIcon)
            : null,
      );

      return locale == null || !locale.isSupportedByDelegates()
          ? dialog
          : Localizations.override(
              context: context, locale: locale, child: dialog);
    }

    if (open && (open != lastOpen)) {
      control.updateProperties({"_open": open}, python: false);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog<DateTime>(
            barrierDismissible: !control.getBool("modal", false)!,
            barrierColor: control.getColor("barrier_color", context),
            useRootNavigator: false,
            context: context,
            builder: (context) => createSelectDateDialog()).then((result) {
          debugPrint("pickDate() completed");
          onClosed(result);
        });
      });
    }
    return const SizedBox.shrink();
  }
}
