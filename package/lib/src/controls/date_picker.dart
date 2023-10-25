import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import 'form_field.dart';

class DatePickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final dynamic dispatch;

  const DatePickerControl({
    Key? key,
    this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.dispatch,
  }) : super(key: key);

  @override
  State<DatePickerControl> createState() => _DatePickerControlState();
}

class _DatePickerControlState extends State<DatePickerControl> {
  String? _state;

  @override
  Widget build(BuildContext context) {
    debugPrint("DatePicker build: ${widget.control.id}");

    String state = widget.control.attrString("state") ?? "initState";
    DateTime? value = widget.control.attrDateTime("value");
    DateTime? firstDate = widget.control.attrDateTime("firstDate");
    DateTime? lastDate = widget.control.attrDateTime("lastDate");
    String? localeString = widget.control.attrString("locale");
    String? helpText = widget.control.attrString("helpText");
    String? cancelText = widget.control.attrString("cancelText");
    String? confirmText = widget.control.attrString("confirmText");
    TextInputType keyboardType =
        parseTextInputType(widget.control.attrString("keyboardType", "")!);
    DatePickerMode datePickerMode =
        parseDatePickerMode(widget.control.attrString("datePickerMode", "")!);
    DatePickerEntryMode datePickerEntryMode = parseDatePickerEntryMode(
        widget.control.attrString("datePickerEntryMode", "")!);
    String? hintText = widget.control.attrString("hintText");

    Locale locale;
    if (localeString == null) {
      locale = Localizations.localeOf(context);
    } else {
      locale = Locale(localeString);
    }

    void onChanged(DateTime? dateValue) {
      debugPrint("New date: $dateValue");
      var newState = "initState";
      String stringValue = dateValue?.toIso8601String() ?? "";
      List<Map<String, String>> props = [
        {"i": widget.control.id, "value": stringValue, "state": newState}
      ];
      widget.dispatch(
          UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
      FletAppServices.of(context).server.updateControlProps(props: props);
      FletAppServices.of(context).server.sendPageEvent(
          eventTarget: widget.control.id,
          eventName: "change",
          eventData: stringValue);
    }

    void onDismissed() {
      var newState = "initState";
      String stringValue = value?.toIso8601String() ?? "";
      List<Map<String, String>> props = [
        {"i": widget.control.id, "value": stringValue, "state": newState}
      ];
      widget.dispatch(
          UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
      FletAppServices.of(context).server.updateControlProps(props: props);

      FletAppServices.of(context).server.sendPageEvent(
          eventTarget: widget.control.id,
          eventName: "dismiss",
          eventData: stringValue);
    }

    Widget createSelectDateDialog() {
      Widget dialog = DatePickerDialog(
        initialDate: value ?? DateTime.now(),
        firstDate: firstDate ?? DateTime(1900),
        lastDate: lastDate ?? DateTime(2050),
        helpText: helpText,
        cancelText: cancelText,
        confirmText: confirmText,
        keyboardType: keyboardType,
        initialCalendarMode: datePickerMode,
        initialEntryMode: datePickerEntryMode,
        fieldHintText: hintText,
      );

      dialog = Localizations.override(
        context: context,
        locale: locale,
        child: dialog,
      );

      return dialog;
    }

    if (_state != state) {
      switch (state) {
        case "pickDate":
          WidgetsBinding.instance.addPostFrameCallback((_) {
            showDialog<DateTime>(
                context: context,
                builder: (context) => createSelectDateDialog()).then((result) {
              debugPrint("pickDate() completed");
              if (result != null) {
                onChanged(result);
              } else {
                onDismissed();
              }
            });
          });
          break;
      }
    }
    return const SizedBox.shrink();
  }
}

DatePickerMode parseDatePickerMode(String mode) {
  switch (mode.toLowerCase()) {
    case "day":
      return DatePickerMode.day;
    case "year":
      return DatePickerMode.year;
  }
  return DatePickerMode.day;
}

DatePickerEntryMode parseDatePickerEntryMode(String mode) {
  switch (mode.toLowerCase()) {
    case "calendar":
      return DatePickerEntryMode.calendar;
    case "input":
      return DatePickerEntryMode.input;
    case "calendarOnly":
      return DatePickerEntryMode.calendarOnly;
    case "inputOnly":
      return DatePickerEntryMode.inputOnly;
  }
  return DatePickerEntryMode.calendar;
}
