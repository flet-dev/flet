import 'package:flet/src/utils/icons.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';

class TimePickerControl extends StatelessWidget {
  final Control control;

  const TimePickerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("TimePicker build: ${control.id}");

    bool lastOpen = control.getBool("_open", false)!;

    var open = control.getBool("open", false)!;
    var value = control.getTimeOfDay("value", TimeOfDay.now())!;
    var hourFormat = control.getString("hour_format");
    var switchToTimerEntryModeIcon =
        control.getIconData("switch_to_timer_icon");
    var switchToInputEntryModeIcon =
        control.getIconData("switch_to_input_icon");

    void onClosed(TimeOfDay? timeValue) {
      control.updateProperties({"_open": false}, python: false);
      control.updateProperties({"value": timeValue, "open": false});
      if (timeValue != null) {
        control.triggerEvent("change", timeValue);
      }
      control.triggerEvent("dismiss", timeValue == null);
    }

    Widget createSelectTimeDialog() {
      Widget dialog = TimePickerDialog(
        initialTime: value,
        helpText: control.getString("help_text"),
        cancelText: control.getString("cancel_text"),
        confirmText: control.getString("confirm_text"),
        hourLabelText: control.getString("hour_label_text"),
        minuteLabelText: control.getString("minute_label_text"),
        errorInvalidText: control.getString("error_invalid_text"),
        initialEntryMode: control.getTimePickerEntryMode(
            "entry_mode", TimePickerEntryMode.dial)!,
        orientation: control.getOrientation("orientation"),
        switchToTimerEntryModeIcon: switchToTimerEntryModeIcon != null
            ? Icon(switchToTimerEntryModeIcon)
            : null,
        switchToInputEntryModeIcon: switchToInputEntryModeIcon != null
            ? Icon(switchToInputEntryModeIcon)
            : null,
        onEntryModeChanged: (TimePickerEntryMode mode) {
          control.updateProperties({"entry_mode": mode.name});
          control.triggerEvent("entry_mode_change", {"entry_mode": mode.name});
        },
      );

      final hourFormatMap = {"h12": false, "h24": true, "system": null};
      return MediaQuery(
        data: MediaQuery.of(context)
            .copyWith(alwaysUse24HourFormat: hourFormatMap[hourFormat]),
        child: dialog,
      );
    }

    if (open && (open != lastOpen)) {
      control.updateProperties({"_open": open}, python: false);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog<TimeOfDay>(
            barrierColor: control.getColor("barrier_color", context),
            barrierDismissible: !control.getBool("modal", false)!,
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
