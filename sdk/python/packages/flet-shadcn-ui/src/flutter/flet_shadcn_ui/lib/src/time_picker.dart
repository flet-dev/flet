import 'package:flet/flet.dart';
import 'package:flutter/material.dart' show TimeOfDay;
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/field.dart';
import 'utils/intrinsics.dart';

class ShadTimePickerControl extends StatefulWidget {
  final Control control;

  const ShadTimePickerControl({super.key, required this.control});

  @override
  State<ShadTimePickerControl> createState() => _ShadTimePickerControlState();
}

class _ShadTimePickerControlState extends State<ShadTimePickerControl> {
  ShadTimePickerController? _controller;
  bool? _period;
  TimeOfDay? _value;

  // ShadTimePicker reports every controller change through onChanged, so a
  // value set from Python is not echoed back as a change event.
  bool _settingValue = false;

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  /// Copies [time] into the controller, as 12-hour time when [period].
  ///
  /// Seconds are not shown, but ShadTimePicker only reports a value once
  /// hours, minutes and seconds are all set, so seconds stay at 0.
  void _setController(TimeOfDay? time, bool period) {
    final c = _controller!;
    if (time == null) {
      c.hour = null;
      c.minute = null;
      c.period = null;
    } else if (period) {
      c.hour = time.hour % 12 == 0 ? 12 : time.hour % 12;
      c.minute = time.minute;
      c.period = time.hour < 12 ? ShadDayPeriod.am : ShadDayPeriod.pm;
    } else {
      c.hour = time.hour;
      c.minute = time.minute;
      c.period = null;
    }
    c.second = 0;
  }

  void _onChanged(ShadTimeOfDay time) {
    if (_settingValue) return;
    var hour = time.hour;
    if (_period == true) {
      hour = hour % 12 + (time.period == ShadDayPeriod.pm ? 12 : 0);
    }
    final value = TimeOfDay(hour: hour, minute: time.minute);
    if (value == _value) return;
    _value = value;
    widget.control.updateProperties({"value": value});
    widget.control.triggerEvent("change");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadTimePicker build: ${widget.control.id}");

    final control = widget.control;
    final period = control.getBool("period", false)!;
    final value = control.getTimeOfDay("value");

    var rebuild = false;
    if (_controller == null || _period != period) {
      _controller?.dispose();
      _controller = ShadTimePickerController();
      _period = period;
      _setController(value, period);
      _value = value;
      rebuild = true;
    } else if (value != _value) {
      _value = value;
      _settingValue = true;
      _setController(value, period);
      _settingValue = false;
      // The controller's fields are not re-read by the text fields, so the
      // picker is rebuilt to show a value set from Python.
      rebuild = true;
    }
    if (rebuild) _generation++;

    final hourLabel = control.buildTextOrWidget("hour_label");
    final minuteLabel = control.buildTextOrWidget("minute_label");
    Widget picker(ShadDecoration? decoration) => period
        ? ShadTimePicker.period(
            key: ValueKey(_generation),
            controller: _controller,
            enabled: !control.disabled,
            showSeconds: false,
            hourLabel: hourLabel,
            minuteLabel: minuteLabel,
            fieldDecoration: decoration,
            onChanged: _onChanged,
          )
        : ShadTimePicker(
            key: ValueKey(_generation),
            controller: _controller,
            enabled: !control.disabled,
            showSeconds: false,
            hourLabel: hourLabel,
            minuteLabel: minuteLabel,
            fieldDecoration: decoration,
            onChanged: _onChanged,
          );

    return LayoutControl(
      control: control,
      child: MeasuredIntrinsics(
        estimate: const Size(220, 70),
        child: buildShadField(context, control, picker),
      ),
    );
  }

  int _generation = 0;
}
