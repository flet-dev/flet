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

    var open = widget.control.attrBool("open", false)!;
    DateTime? value = widget.control.attrDateTime("value");
    DateTime? currentDate = widget.control.attrDateTime("currentDate");
    IconData? switchToCalendarEntryModeIcon = parseIcon(
        widget.control.attrString("switchToCalendarEntryModeIcon", "")!);
    IconData? switchToInputEntryModeIcon =
        parseIcon(widget.control.attrString("switchToInputEntryModeIcon"));

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
        firstDate: widget.control.attrDateTime("firstDate", DateTime(1900))!,
        lastDate: widget.control.attrDateTime("lastDate", DateTime(2050))!,
        currentDate: currentDate ?? DateTime.now(),
        helpText: widget.control.attrString("helpText"),
        cancelText: widget.control.attrString("cancelText"),
        confirmText: widget.control.attrString("confirmText"),
        errorFormatText: widget.control.attrString("errorFormatText"),
        errorInvalidText: widget.control.attrString("errorInvalidText"),
        keyboardType: parseTextInputType(
            widget.control.attrString("keyboardType"), TextInputType.text)!,
        initialCalendarMode: parseDatePickerMode(
            widget.control.attrString("datePickerMode"), DatePickerMode.day)!,
        initialEntryMode: parseDatePickerEntryMode(
            widget.control.attrString("datePickerEntryMode"),
            DatePickerEntryMode.calendar)!,
        fieldHintText: widget.control.attrString("fieldHintText"),
        fieldLabelText: widget.control.attrString("fieldLabelText"),
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
            barrierColor: widget.control.attrColor("barrierColor", context),
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
