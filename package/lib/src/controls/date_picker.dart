import 'package:flutter/material.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/icons.dart';
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
  @override
  Widget build(BuildContext context) {
    debugPrint("DatePicker build: ${widget.control.id}");

    bool lastOpen = widget.control.state["open"] ?? false;

    var open = widget.control.attrBool("open", false)!;
    DateTime? value = widget.control.attrDateTime("value");
    DateTime? firstDate = widget.control.attrDateTime("firstDate");
    DateTime? lastDate = widget.control.attrDateTime("lastDate");
    DateTime? currentDate = widget.control.attrDateTime("currentDate");
    //String? localeString = widget.control.attrString("locale");
    String? helpText = widget.control.attrString("helpText");
    String? cancelText = widget.control.attrString("cancelText");
    String? confirmText = widget.control.attrString("confirmText");
    String? errorFormatText = widget.control.attrString("errorFormatText");
    String? errorInvalidText = widget.control.attrString("errorInvalidText");
    TextInputType keyboardType =
        parseTextInputType(widget.control.attrString("keyboardType", "")!);
    DatePickerMode datePickerMode = DatePickerMode.values.firstWhere(
        (a) =>
            a.name.toLowerCase() ==
            widget.control.attrString("datePickerMode", "")!.toLowerCase(),
        orElse: () => DatePickerMode.day);
    DatePickerEntryMode datePickerEntryMode = DatePickerEntryMode.values
        .firstWhere(
            (a) =>
                a.name.toLowerCase() ==
                widget.control
                    .attrString("datePickerEntryMode", "")!
                    .toLowerCase(),
            orElse: () => DatePickerEntryMode.calendar);
    String? fieldHintText = widget.control.attrString("fieldHintText");
    String? fieldLabelText = widget.control.attrString("fieldLabelText");
    IconData? switchToCalendarEntryModeIcon = getMaterialIcon(
        widget.control.attrString("switchToCalendarEntryModeIcon", "")!);
    IconData? switchToInputEntryModeIcon = getMaterialIcon(
        widget.control.attrString("switchToInputEntryModeIcon", "")!);

    //Locale locale;
    // if (localeString == null) {
    //   locale = Localizations.localeOf(context);
    // } else {
    //   //locale = Locale(localeString);
    // }

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
      Widget dialog = DatePickerDialog(
        initialDate: value ?? currentDate ?? DateTime.now(),
        firstDate: firstDate ?? DateTime(1900),
        lastDate: lastDate ?? DateTime(2050),
        currentDate: currentDate ?? DateTime.now(),
        helpText: helpText,
        cancelText: cancelText,
        confirmText: confirmText,
        errorFormatText: errorFormatText,
        errorInvalidText: errorInvalidText,
        keyboardType: keyboardType,
        initialCalendarMode: datePickerMode,
        initialEntryMode: datePickerEntryMode,
        fieldHintText: fieldHintText,
        fieldLabelText: fieldLabelText,
        switchToCalendarEntryModeIcon: switchToCalendarEntryModeIcon != null
            ? Icon(switchToCalendarEntryModeIcon)
            : null,
        switchToInputEntryModeIcon: switchToInputEntryModeIcon != null
            ? Icon(switchToInputEntryModeIcon)
            : null,
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
        showDialog<DateTime>(
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
