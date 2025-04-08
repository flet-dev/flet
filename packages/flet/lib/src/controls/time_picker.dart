import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';

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

    bool lastOpen = widget.control.state["open"] ?? false;

    var open = widget.control.getBool("open", false)!;
    TimeOfDay value = widget.control.getTime("value", TimeOfDay.now())!;

    void onClosed(TimeOfDay? timeValue) {
      String stringValue;
      String eventName;
      if (timeValue == null) {
        String hourString = value.hour.toString();
        String minuteString = value.minute.toString();
        stringValue = '$hourString:$minuteString';
        eventName = "dismiss";
      } else {
        String hourString = timeValue.hour.toString();
        String minuteString = timeValue.minute.toString();
        stringValue = '$hourString:$minuteString';
        eventName = "change";
      }
      widget.control.state["open"] = false;
      FletBackend.of(context).updateControl(
          widget.control.id, {"value": stringValue, "open": "false"});
      FletBackend.of(context)
          .triggerControlEvent(widget.control, eventName, stringValue);
    }

    Widget createSelectTimeDialog() {
      Widget dialog = TimePickerDialog(
        initialTime: value,
        helpText: widget.control.getString("helpText"),
        cancelText: widget.control.getString("cancelText"),
        confirmText: widget.control.getString("confirmText"),
        hourLabelText: widget.control.getString("hourLabelText"),
        minuteLabelText: widget.control.getString("minuteLabelText"),
        errorInvalidText: widget.control.getString("errorInvalidText"),
        initialEntryMode: widget.control.getTimePickerEntryMode(
            "timePickerEntryMode", TimePickerEntryMode.dial)!,
        orientation: parseOrientation(widget.control.getString("orientation")),
        onEntryModeChanged: (TimePickerEntryMode mode) {
          FletBackend.of(context).triggerControlEvent(
              widget.control, "entry_mode_change", mode.name);
        },
      );

      return dialog;
    }

    if (open && (open != lastOpen)) {
      widget.control.state["open"] = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog<TimeOfDay>(
            barrierColor: widget.control.getColor("barrierColor", context),
            useRootNavigator: false,
            context: context,
            builder: (context) => createSelectTimeDialog()).then((result) {
          debugPrint("pickTime() completed");
          onClosed(result);
        });
      });
    }
    return const SizedBox.shrink();
  }
}
