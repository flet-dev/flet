import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/form_field.dart';
import '../utils/icons.dart';
import '../utils/others.dart';

class DatePickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final FletControlBackend backend;

  const DatePickerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.backend});

  @override
  State<DatePickerControl> createState() => _DatePickerControlState();
}

class _DatePickerControlState extends State<DatePickerControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("DatePicker build: ${widget.control.id}");

    bool lastOpen = widget.control.state["open"] ?? false;

    var open = widget.control.getBool("open", false)!;
    DateTime? value = widget.control.getDateTime("value");
    DateTime? currentDate = widget.control.getDateTime("currentDate");
    IconData? switchToCalendarEntryModeIcon = parseIcon(
        widget.control.getString("switchToCalendarEntryModeIcon", "")!);
    IconData? switchToInputEntryModeIcon =
        parseIcon(widget.control.getString("switchToInputEntryModeIcon"));

    void onClosed(DateTime? dateValue) {
      String stringValue;
      String eventName;
      if (dateValue == null) {
        stringValue =
            value?.toIso8601String() ?? currentDate?.toIso8601String() ?? "";
        eventName = "dismiss";
      } else {
        stringValue = dateValue.toIso8601String();
        eventName = "change";
      }
      widget.control.state["open"] = false;
      widget.backend.updateControlState(
          widget.control.id, {"value": stringValue, "open": "false"});
      widget.backend
          .triggerControlEvent(widget.control.id, eventName, stringValue);
    }

    Widget createSelectDateDialog() {
      Widget dialog = DatePickerDialog(
        initialDate: value ?? currentDate ?? DateTime.now(),
        firstDate: widget.control.getDateTime("firstDate", DateTime(1900))!,
        lastDate: widget.control.getDateTime("lastDate", DateTime(2050))!,
        currentDate: currentDate ?? DateTime.now(),
        helpText: widget.control.getString("helpText"),
        cancelText: widget.control.getString("cancelText"),
        confirmText: widget.control.getString("confirmText"),
        errorFormatText: widget.control.getString("errorFormatText"),
        errorInvalidText: widget.control.getString("errorInvalidText"),
        keyboardType: parseTextInputType(
            widget.control.getString("keyboardType"), TextInputType.text)!,
        initialCalendarMode: parseDatePickerMode(
            widget.control.getString("datePickerMode"), DatePickerMode.day)!,
        initialEntryMode: parseDatePickerEntryMode(
            widget.control.getString("datePickerEntryMode"),
            DatePickerEntryMode.calendar)!,
        fieldHintText: widget.control.getString("fieldHintText"),
        fieldLabelText: widget.control.getString("fieldLabelText"),
        onDatePickerModeChange: (DatePickerEntryMode mode) {
          widget.backend.triggerControlEvent(
              widget.control.id, "entryModeChange", mode.name);
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
      widget.control.state["open"] = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog<DateTime>(
            barrierColor: widget.control.getColor("barrierColor", context),
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
