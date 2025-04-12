import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../controls/control_widget.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';

class CupertinoBottomSheetControl extends StatelessWidget {
  final Control control;

  const CupertinoBottomSheetControl({
    super.key,
    required this.control,
  });

  Widget _createDialog(BuildContext context) {
    Control? content = control.child("content");

    if (content == null) {
      return const ErrorControl("CupertinoButtomSheet.content is empty.");
    }

    Widget child = ControlWidget(control: content);

    if (["CupertinoPicker", "CupertinoTimerPicker", "CupertinoDatePicker"]
        .contains(content.type)) {
      child = Container(
        height: control.getDouble("height", 220.0)!,
        padding: control.getPadding("padding"),
        // bottom margin is provided to align the popup above the system navigation bar
        margin:
            EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
        // popup background color
        color: control.getColor("bgcolor", context,
            CupertinoColors.systemBackground.resolveFrom(context))!,
        // Use SafeArea to avoid system overlaps
        child: SafeArea(
          top: false,
          child: child,
        ),
      );
    }

    return Material(child: child);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoBottomSheet build: ${control.id}");

    bool lastOpen = control.getBool("_open", false)!;

    var open = control.getBool("open", false)!;

    if (open && (open != lastOpen)) {
      var dialog = _createDialog(context);
      if (dialog is ErrorControl) {
        return dialog;
      }

      control.updateProperties({"_open": open}, python: false);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showCupertinoModalPopup(
            barrierDismissible: !control.getBool("modal", false)!,
            useRootNavigator: false,
            context: context,
            builder: (context) => dialog).then((value) {
          debugPrint("Dismiss CupertinoBottomSheet: $lastOpen");
          control.updateProperties({"_open": false}, python: false);
          control.updateProperties({"open": false});
          control.triggerEvent("dismiss");
        });
      });
    } else if (open != lastOpen && lastOpen && Navigator.of(context).canPop()) {
      Navigator.of(context).pop();
    }

    return const SizedBox.shrink();
  }
}
