import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';

class TimePickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const TimePickerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  State<TimePickerControl> createState() => _TimePickerControlState();
}

class _TimePickerControlState extends State<TimePickerControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("TimePicker build: ${widget.control.id}");

    bool lastOpen = widget.control.state["open"] ?? false;

    var open = widget.control.attrBool("open", false)!;
    TimeOfDay value = widget.control.attrTime("value") ?? TimeOfDay.now();
    String? helpText = widget.control.attrString("helpText");
    String? cancelText = widget.control.attrString("cancelText");
    String? confirmText = widget.control.attrString("confirmText");
    String? hourLabelText = widget.control.attrString("hourLabelText");
    String? minuteLabelText = widget.control.attrString("minuteLabelText");
    String? errorInvalidText = widget.control.attrString("errorInvalidText");
    TimePickerEntryMode timePickerEntryMode = TimePickerEntryMode.values
        .firstWhere(
            (a) =>
                a.name.toLowerCase() ==
                widget.control
                    .attrString("timePickerEntryMode", "")!
                    .toLowerCase(),
            orElse: () => TimePickerEntryMode.dial);
    Orientation? orientation = Orientation.values.firstWhereOrNull((a) =>
        a.name.toLowerCase() ==
        widget.control.attrString("orientation", "")!.toLowerCase());

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
      widget.backend.updateControlState(
          widget.control.id, {"value": stringValue, "open": "false"});
      widget.backend
          .triggerControlEvent(widget.control.id, eventName, stringValue);
    }

    Widget createSelectTimeDialog() {
      Widget dialog = TimePickerDialog(
        initialTime: value,
        helpText: helpText,
        cancelText: cancelText,
        confirmText: confirmText,
        hourLabelText: hourLabelText,
        minuteLabelText: minuteLabelText,
        errorInvalidText: errorInvalidText,
        initialEntryMode: timePickerEntryMode,
        orientation: orientation,
        onEntryModeChanged: (TimePickerEntryMode mode) {
          widget.backend.triggerControlEvent(
              widget.control.id, "entryModeChange", mode.name);
        },
      );

      return dialog;
    }

    if (open && (open != lastOpen)) {
      widget.control.state["open"] = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog<TimeOfDay>(
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
