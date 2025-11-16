import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class DatePickerControl extends StatefulWidget {
  final Control control;

  DatePickerControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<DatePickerControl> createState() => _DatePickerControlState();
}

class _DatePickerControlState extends State<DatePickerControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("DatePicker build: ${widget.control.id}");

    bool lastOpen = widget.control.getBool("_open", false)!;

    var open = widget.control.getBool("open", false)!;
    var value = widget.control.getDateTime("value");
    var currentDate = widget.control.getDateTime("current_date");
    var switchToCalendarEntryModeIcon =
        widget.control.getIconData("switch_to_calendar_icon");
    var switchToInputEntryModeIcon =
        widget.control.getIconData("switch_to_input_icon");

    void onClosed(DateTime? dateValue) {
      widget.control.updateProperties({"_open": false}, python: false);
      widget.control
          .updateProperties({"value": dateValue ?? value, "open": false});
      if (dateValue != null) {
        widget.control.triggerEvent("change", dateValue);
      }
      widget.control.triggerEvent("dismiss", dateValue == null);
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
            "entry_mode", DatePickerEntryMode.calendar)!,
        fieldHintText: widget.control.getString("field_hint_text"),
        fieldLabelText: widget.control.getString("field_label_text"),
        insetPadding: widget.control.getPadding("inset_padding",
            const EdgeInsets.symmetric(horizontal: 16.0, vertical: 24.0))!,
        onDatePickerModeChange: (DatePickerEntryMode mode) {
          widget.control.updateProperties({"entry_mode": mode.name});
          widget.control
              .triggerEvent("entry_mode_change", {"entry_mode": mode.name});
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
