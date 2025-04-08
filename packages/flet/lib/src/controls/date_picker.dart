import 'package:flet/src/utils/colors.dart';
import 'package:flet/src/utils/misc.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/form_field.dart';
import '../utils/icons.dart';

class DatePickerControl extends StatefulWidget {
  final Control control;

  const DatePickerControl({
    super.key,
    required this.control,
  });

  @override
  State<DatePickerControl> createState() => _DatePickerControlState();
}

class _DatePickerControlState extends State<DatePickerControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("DatePicker build: ${widget.control.id}");

    bool lastOpen = widget.control.getBool("_open", false)!;

    var open = widget.control.getBool("open", false)!;
    DateTime? value = widget.control.getDateTime("value");
    DateTime? currentDate = widget.control.getDateTime("currentDate");
    IconData? switchToCalendarEntryModeIcon = parseIcon(
        widget.control.getString("switchToCalendarEntryModeIcon", "")!);
    IconData? switchToInputEntryModeIcon =
        parseIcon(widget.control.getString("switchToInputEntryModeIcon"));

    void onClosed(DateTime? dateValue) {
      widget.control.updateProperties({"_open": false}, python: false);
      widget.control
          .updateProperties({"value": dateValue ?? value, "open": false});
      widget.control.triggerEvent(
          dateValue == null ? "dismiss" : "change", dateValue ?? value);
    }

    Widget createSelectDateDialog() {
      Widget dialog = DatePickerDialog(
        initialDate: value ?? currentDate ?? DateTime.now(),
        firstDate: widget.control.getDateTime("first_date", DateTime(1900))!,
        lastDate: widget.control.getDateTime("last_date", DateTime(2050))!,
        currentDate: currentDate ?? DateTime.now(),
        helpText: widget.control.getString("help_text"),
        cancelText: widget.control.getString("cancel_text"),
        confirmText: widget.control.getString("confirm_text"),
        errorFormatText: widget.control.getString("error_format_text"),
        errorInvalidText: widget.control.getString("error_invalid_text"),
        keyboardType: parseTextInputType(
            widget.control.getString("keyboard_type"), TextInputType.text)!,
        initialCalendarMode: widget.control
            .getDatePickerMode("date_picker_mode", DatePickerMode.day)!,
        initialEntryMode: widget.control.getDatePickerEntryMode(
            "date_picker_entry_mode", DatePickerEntryMode.calendar)!,
        fieldHintText: widget.control.getString("field_hint_text"),
        fieldLabelText: widget.control.getString("field_label_text"),
        onDatePickerModeChange: (DatePickerEntryMode mode) {
          widget.control.triggerEvent("entry_mode_change", mode.name);
        },
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
        showDialog<DateTime>(
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
