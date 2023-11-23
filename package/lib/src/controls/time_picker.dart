import 'package:flutter/material.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/icons.dart';
import 'form_field.dart';

class TimePickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final dynamic dispatch;

  const TimePickerControl({
    Key? key,
    this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.dispatch,
  }) : super(key: key);

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
    String? errorFormatText = widget.control.attrString("errorFormatText");
    String? errorInvalidText = widget.control.attrString("errorInvalidText");
    TimePickerEntryMode timePickerEntryMode = TimePickerEntryMode.values
        .firstWhere(
            (a) =>
                a.name.toLowerCase() ==
                widget.control
                    .attrString("timePickerEntryMode", "")!
                    .toLowerCase(),
            orElse: () => TimePickerEntryMode.dial);
    String? fieldHintText = widget.control.attrString("fieldHintText");
    String? fieldLabelText = widget.control.attrString("fieldLabelText");

    void onClosed(TimeOfDay? timeValue) {
      String stringValue;
      String eventName;
      if (timeValue == null) {
        // stringValue =
        //     value?.toIso8601String() ?? currentDate?.toIso8601String() ?? "";
        // stringValue = value?.toString() ?? TimeOfDay.now().toString();
        String? hourString = value?.hour.toString();
        String? minuteString = value?.minute.toString();
        stringValue = '$hourString:$minuteString';
        eventName = "dismiss";
      } else {
        String? hourString = timeValue.hour.toString();
        String? minuteString = timeValue.minute.toString();
        stringValue = '$hourString:$minuteString';
        //stringValue = timeValue.toString();
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

    Widget createSelectDateDialog() {
      Widget dialog = TimePickerDialog(
        initialTime: value,
        //initialDate: value ?? currentDate ?? DateTime.now(),
        //firstDate: firstDate ?? DateTime(1900),
        //lastDate: lastDate ?? DateTime(2050),
        //currentDate: currentDate ?? DateTime.now(),
        helpText: helpText,
        cancelText: cancelText,
        confirmText: confirmText,
        //errorFormatText: errorFormatText,
        errorInvalidText: errorInvalidText,
        //keyboardType: keyboardType,
        //initialCalendarMode: datePickerMode,
        initialEntryMode: timePickerEntryMode,
        //fieldHintText: fieldHintText,
        //fieldLabelText: fieldLabelText,
        //switchToCalendarEntryModeIcon: switchToCalendarEntryModeIcon != null
        //    ? Icon(switchToCalendarEntryModeIcon)
        //    : null,
        //switchToInputEntryModeIcon: switchToInputEntryModeIcon != null
        //    ? Icon(switchToInputEntryModeIcon)
        //    : null,
      );

      // dialog = Localizations.override(
      //   context: context,
      //   locale: locale,
      //   child: dialog,
      // );

      return dialog;
    }

    if (open && (open != lastOpen)) {
      widget.control.state["open"] = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        //showDialog<DateTime>(
        showDialog<TimeOfDay>(
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
