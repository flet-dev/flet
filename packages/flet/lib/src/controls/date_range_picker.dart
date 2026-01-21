import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/form_field.dart';
import '../utils/icons.dart';
import '../utils/locale.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';

class DateRangePickerControl extends StatelessWidget {
  final Control control;

  const DateRangePickerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("DateRangePicker build: ${control.id}");

    bool lastOpen = control.getBool("_open", false)!;

    var open = control.getBool("open", false)!;
    var currentDate = control.getDateTime("current_date");
    var startValue = control.getDateTime("start_value");
    var endValue = control.getDateTime("end_value");
    var value = DateTimeRange<DateTime>(
        start: startValue ?? currentDate ?? DateTime.now(),
        end: endValue ?? currentDate ?? DateTime.now());

    var switchToCalendarEntryModeIcon =
        control.getIconData("switch_to_calendar_icon");
    var switchToInputEntryModeIcon =
        control.getIconData("switch_to_input_icon");
    var locale = control.getLocale("locale");

    void onClosed(DateTimeRange<DateTime>? dateRangeValue) {
      control.updateProperties({"_open": false}, python: false);
      var props = {
        "start_value": dateRangeValue?.start ?? startValue,
        "end_value": dateRangeValue?.end ?? endValue,
        "open": false
      };
      control.updateProperties(props);
      if (dateRangeValue != null) {
        control.triggerEvent("change", dateRangeValue);
      }
      control.triggerEvent("dismiss", dateRangeValue == null);
    }

    Widget createSelectDateDialog() {
      Widget dialog = DateRangePickerDialog(
        initialDateRange: value,
        firstDate: control.getDateTime("first_date", DateTime(1900))!,
        lastDate: control.getDateTime("last_date", DateTime(2050))!,
        currentDate: currentDate ?? DateTime.now(),
        helpText: control.getString("help_text"),
        cancelText: control.getString("cancel_text"),
        confirmText: control.getString("confirm_text"),
        saveText: control.getString("save_text"),
        errorInvalidRangeText: control.getString("error_invalid_range_text"),
        errorFormatText: control.getString("error_format_text"),
        errorInvalidText: control.getString("error_invalid_text"),
        fieldStartHintText: control.getString("field_start_hint_text"),
        fieldEndHintText: control.getString("field_end_hint_text"),
        fieldStartLabelText: control.getString("field_start_label_text"),
        fieldEndLabelText: control.getString("field_end_label_text"),
        keyboardType: parseTextInputType(
            control.getString("keyboard_type"), TextInputType.text)!,
        initialEntryMode: control.getDatePickerEntryMode(
            "entry_mode", DatePickerEntryMode.calendar)!,
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
        showDialog<DateTimeRange<DateTime>>(
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
