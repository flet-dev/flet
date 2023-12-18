import 'package:flutter/material.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';

class TimePickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final dynamic dispatch;

  const TimePickerControl({
    super.key,
    this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.dispatch,
  });

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
      List<Map<String, String>> props = [
        {"i": widget.control.id, "value": stringValue, "open": "false"}
      ];
      widget.dispatch(
          UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
      FletAppServices.of(context).server.updateControlProps(props: props);

      FletAppServices.of(context).server.sendPageEvent(
          eventTarget: widget.control.id,
          eventName: eventName,
          eventData: stringValue);
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
