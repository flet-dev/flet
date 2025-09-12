import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/form_field.dart';
import '../utils/icons.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';

class DateRangePickerControl extends StatefulWidget {
  final Control control;

  DateRangePickerControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<DateRangePickerControl> createState() => _DateRangePickerControlState();
}

class _DateRangePickerControlState extends State<DateRangePickerControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("DateRangePicker build: ${widget.control.id}");

    bool lastOpen = widget.control.getBool("_open", false)!;

    var open = widget.control.getBool("open", false)!;
    var currentDate = widget.control.getDateTime("current_date");
    var startValue = widget.control.getDateTime("start_value");
    var endValue = widget.control.getDateTime("end_value");
    var value = DateTimeRange<DateTime>(
        start: startValue ?? currentDate ?? DateTime.now(),
        end: endValue ?? currentDate ?? DateTime.now());

    var switchToCalendarEntryModeIcon =
        widget.control.getIconData("switch_to_calendar_icon");
    var switchToInputEntryModeIcon =
        widget.control.getIconData("switch_to_input_icon");

    void onClosed(DateTimeRange<DateTime>? dateRangeValue) {
      widget.control.updateProperties({"_open": false}, python: false);
      var props = {
        "start_value": dateRangeValue?.start ?? startValue,
        "end_value": dateRangeValue?.end ?? endValue,
        "open": false
      };
      widget.control.updateProperties(props);
      if (dateRangeValue != null) {
        widget.control.triggerEvent("change", dateRangeValue);
      }
      widget.control.triggerEvent("dismiss", dateRangeValue == null);
    }

    Widget createSelectDateDialog() {
      Widget dialog = DateRangePickerDialog(
        initialDateRange: value,
        firstDate: widget.control.getDateTime("first_date", DateTime(1900))!,
        lastDate: widget.control.getDateTime("last_date", DateTime(2050))!,
        currentDate: currentDate ?? DateTime.now(),
        helpText: widget.control.getString("help_text"),
        cancelText: widget.control.getString("cancel_text"),
        confirmText: widget.control.getString("confirm_text"),
        saveText: widget.control.getString("save_text"),
        errorInvalidRangeText:
            widget.control.getString("error_invalid_range_text"),
        errorFormatText: widget.control.getString("error_format_text"),
        errorInvalidText: widget.control.getString("error_invalid_text"),
        fieldStartHintText: widget.control.getString("field_start_hint_text"),
        fieldEndHintText: widget.control.getString("field_end_hint_text"),
        fieldStartLabelText: widget.control.getString("field_start_label_text"),
        fieldEndLabelText: widget.control.getString("field_end_label_text"),
        keyboardType: parseTextInputType(
            widget.control.getString("keyboard_type"), TextInputType.text)!,
        initialEntryMode: widget.control.getDatePickerEntryMode(
            "date_picker_entry_mode", DatePickerEntryMode.calendar)!,
        switchToCalendarEntryModeIcon: switchToCalendarEntryModeIcon != null
            ? Icon(switchToCalendarEntryModeIcon)
            : null,
        switchToInputEntryModeIcon: switchToInputEntryModeIcon != null
            ? Icon(switchToInputEntryModeIcon)
            : null,
      );

      return dialog;
    }

    if (open && (open != lastOpen)) {
      widget.control.updateProperties({"_open": open}, python: false);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog<DateTimeRange<DateTime>>(
            barrierDismissible: !widget.control.getBool("modal", false)!,
            barrierColor: widget.control.getColor("barrier_color", context),
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
