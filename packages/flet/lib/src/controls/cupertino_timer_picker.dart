import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import 'error.dart';

class CupertinoTimerPickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final Widget? nextChild;

  final FletControlBackend backend;

  const CupertinoTimerPickerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.nextChild,
      required this.backend});

  @override
  State<CupertinoTimerPickerControl> createState() =>
      _CupertinoTimerPickerControlState();
}

class _CupertinoTimerPickerControlState
    extends State<CupertinoTimerPickerControl> {
  Widget _createPicker() {
    int value = widget.control.attrInt("value", 0)!;
    Duration initialTimerDuration = Duration(milliseconds: value);
    int minuteInterval =
        widget.control.attrDouble("minuteInterval", 1)!.toInt();
    int secondInterval =
        widget.control.attrDouble("secondInterval", 1)!.toInt();
    CupertinoTimerPickerMode mode = CupertinoTimerPickerMode.values.firstWhere(
        (a) =>
            a.name.toLowerCase() ==
            widget.control.attrString("mode", "")!.toLowerCase(),
        orElse: () => CupertinoTimerPickerMode.hms);

    Color? backgroundColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("bgColor", "")!);

    Widget picker = CupertinoTimerPicker(
      mode: mode,
      initialTimerDuration: initialTimerDuration,
      minuteInterval: minuteInterval,
      secondInterval: secondInterval,
      alignment:
          parseAlignment(widget.control, "alignment") ?? Alignment.center,
      backgroundColor: backgroundColor,
      onTimerDurationChanged: (Duration d) {
        widget.backend
            .updateControlState(widget.control.id, {"value": d.toString()});
        widget.backend.triggerControlEvent(
            widget.control.id, "change", d.inMilliseconds.toString());
      },
    );

    return Container(
      height: 216,
      padding: const EdgeInsets.only(top: 6.0),
      // The Bottom margin is provided to align the popup above the system navigation bar.
      margin: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom,
      ),
      // Provide a background color for the popup.
      color: CupertinoColors.systemBackground.resolveFrom(context),
      // Use a SafeArea widget to avoid system overlaps.
      child: SafeArea(
        top: false,
        child: picker,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoTimerPicker build: ${widget.control.id}");

    bool lastOpen = widget.control.state["open"] ?? false;

    var open = widget.control.attrBool("open", false)!;
    var modal = widget.control.attrBool("modal", false)!;

    debugPrint("Current open state: $lastOpen");
    debugPrint("New open state: $open");

    if (open && (open != lastOpen)) {
      var dialog = _createPicker();
      if (dialog is ErrorControl) {
        return dialog;
      }

      // close previous dialog
      if (ModalRoute.of(context)?.isCurrent != true) {
        Navigator.of(context).pop();
      }

      widget.control.state["open"] = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showCupertinoModalPopup(
            barrierDismissible: !modal,
            useRootNavigator: false,
            context: context,
            builder: (context) => _createPicker()).then((value) {
          lastOpen = widget.control.state["open"] ?? false;
          debugPrint("Picker should be dismissed ($hashCode): $lastOpen");
          bool shouldDismiss = lastOpen;
          widget.control.state["open"] = false;

          if (shouldDismiss) {
            widget.backend
                .updateControlState(widget.control.id, {"open": "false"});
            widget.backend
                .triggerControlEvent(widget.control.id, "dismiss", "");
          }
        });
      });
    } else if (open != lastOpen && lastOpen) {
      Navigator.of(context).pop();
    }

    return widget.nextChild ?? const SizedBox.shrink();
  }
}
