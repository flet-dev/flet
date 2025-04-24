import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';

class TimePickerControl extends StatefulWidget {
  final Control control;

  const TimePickerControl({super.key, required this.control});

  @override
  State<TimePickerControl> createState() => _TimePickerControlState();
}

class _TimePickerControlState extends State<TimePickerControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("TimePicker build: ${widget.control.id}");

    bool lastOpen = widget.control.getBool("_open", false)!;

    var open = widget.control.getBool("open", false)!;
    var value = widget.control.getTimeOfDay("value", TimeOfDay.now())!;

    void onClosed(TimeOfDay? timeValue) {
      widget.control.updateProperties({"_open": false}, python: false);
      widget.control.updateProperties({"value": timeValue, "open": false});
      if (timeValue != null) {
        widget.control.triggerEvent("change", data: timeValue);
      }
      widget.control.triggerEvent("dismiss", data: timeValue == null);
    }

    Widget createSelectTimeDialog() {
      Widget dialog = TimePickerDialog(
        initialTime: value,
        helpText: widget.control.getString("help_text"),
        cancelText: widget.control.getString("cancel_text"),
        confirmText: widget.control.getString("confirm_text"),
        hourLabelText: widget.control.getString("hour_label_text"),
        minuteLabelText: widget.control.getString("minute_label_text"),
        errorInvalidText: widget.control.getString("error_invalid_text"),
        initialEntryMode: widget.control.getTimePickerEntryMode(
            "time_picker_entry_mode", TimePickerEntryMode.dial)!,
        orientation: widget.control.getOrientation("orientation"),
        onEntryModeChanged: (TimePickerEntryMode mode) {
          widget.control.triggerEvent("entry_mode_change", data: mode.name);
        },
      );

      return dialog;
    }

    if (open && (open != lastOpen)) {
      widget.control.updateProperties({"_open": open}, python: false);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog<TimeOfDay>(
            barrierColor: widget.control.getColor("barrier_color", context),
            barrierDismissible: !widget.control.getBool("modal", false)!,
            useRootNavigator: false,
            context: context,
            builder: (context) => createSelectTimeDialog()).then((result) {
          onClosed(result);
        });
      });
    }
    return const SizedBox.shrink();
  }
}
