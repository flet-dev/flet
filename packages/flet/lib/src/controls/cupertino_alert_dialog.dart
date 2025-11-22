import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../widgets/control_inherited_notifier.dart';
import '../widgets/error.dart';

class CupertinoAlertDialogControl extends StatelessWidget {
  final Control control;

  const CupertinoAlertDialogControl({super.key, required this.control});

  Widget _createCupertinoAlertDialog() {
    return ControlInheritedNotifier(
      notifier: control,
      child: Builder(builder: (context) {
        ControlInheritedNotifier.of(context);
        var insetAnimation = parseAnimation(
            control.get("inset_animation"),
            ImplicitAnimationDetails(
                duration: const Duration(milliseconds: 100),
                curve: Curves.decelerate))!;

        return CupertinoAlertDialog(
          insetAnimationCurve: insetAnimation.curve,
          insetAnimationDuration: insetAnimation.duration,
          title: control.buildTextOrWidget("title"),
          content: control.buildWidget("content"),
          actions: control.buildWidgets("actions"),
        );
      }),
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoAlertDialog build: ${control.id}");

    final lastOpen = control.getBool("_open", false)!;
    var open = control.getBool("open", false)!;
    var modal = control.getBool("modal", false)!;

    if (open && (open != lastOpen)) {
      if (control.get("title") == null &&
          control.get("content") == null &&
          control.children("actions").isEmpty) {
        return const ErrorControl(
            "CupertinoAlertDialog has nothing to display. Provide at minimum one of the following: title, content, actions.");
      }

      control.updateProperties({"_open": open}, python: false);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog(
            barrierDismissible: !modal,
            barrierColor: control.getColor("barrier_color", context),
            useRootNavigator: false,
            context: context,
            builder: (context) => _createCupertinoAlertDialog()).then((value) {
          debugPrint("Dismissing CupertinoAlertDialog(${control.id})");
          control.updateProperties({"_open": false}, python: false);
          control.updateProperties({"open": false});
          control.triggerEvent("dismiss");
        });
      });
    } else if (!open && lastOpen) {
      if (Navigator.of(context).canPop() == true) {
        debugPrint(
            "CupertinoAlertDialog(${control.id}): Closing dialog managed by this widget.");
        Navigator.of(context).pop();
        control.updateProperties({"_open": false}, python: false);
      } else {
        debugPrint(
            "CupertinoAlertDialog(${control.id}): Dialog was not opened by this widget, skipping pop.");
      }
    }
    return const SizedBox.shrink();
  }
}
