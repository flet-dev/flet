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

  const DatePickerControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<DatePickerControl> createState() => _DatePickerControlState();
}

class _DatePickerControlState extends State<DatePickerControl> {
  DateTime? _value;
  String? _state;

  DateTime? get value {
    return widget.control.attrDateTime("value");
  }

  @override
  void initState() {
    super.initState();
    _value = value;
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("DatePicker build: ${widget.control.id}");

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint("DatePicker StoreConnector build: ${widget.control.id}");

          String state = widget.control.attrString("state") ?? "initState";
          DateTime? firstDate = widget.control.attrDateTime("firstDate");
          DateTime? lastDate = widget.control.attrDateTime("firstDate");
          bool onChange = widget.control.attrBool("onChange", false)!;
          String? localeString = widget.control.attrString("locale");
          String? helpText = widget.control.attrString("helpText");
          String? cancelText = widget.control.attrString("cancelText");
          String? confirmText = widget.control.attrString("confirmText");
          TextInputType keyboardType = parseTextInputType(
              widget.control.attrString("keyboardType", "")!);
          DatePickerMode datePickerMode = parseDatePickerMode(
              widget.control.attrString("datePickerMode", "")!);
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
            setState(() {
              _value = dateValue;
              _state = newState;
            });
            String stringValue = dateValue?.toIso8601String() ?? "";
            List<Map<String, String>> props = [
              {"i": widget.control.id, "value": stringValue, "state": newState}
            ];
            dispatch(UpdateControlPropsAction(
                UpdateControlPropsPayload(props: props)));
            FletAppServices.of(context).server.updateControlProps(props: props);
            if (onChange) {
              FletAppServices.of(context).server.sendPageEvent(
                  eventTarget: widget.control.id,
                  eventName: "change",
                  eventData: stringValue);
            }
            FletAppServices.of(context).server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "submit",
                eventData: "");
          }

          Widget selectDateDialog() {
            Widget dialog = DatePickerDialog(
              initialDate: _value ?? DateTime.now(),
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
                      builder: (context) => selectDateDialog()).then((result) {
                    debugPrint("pickDate() completed");
                    onChanged(result);
                  });
                });
                break;
            }
          }
          return const SizedBox.shrink();
        });
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
