import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../widgets/control_inherited_notifier.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class AlertDialogControl extends StatelessWidget {
  final Control control;

  const AlertDialogControl({super.key, required this.control});

  Widget _createAlertDialog(BuildContext context) {
    return ControlInheritedNotifier(
      notifier: control,
      child: Builder(builder: (context) {
        ControlInheritedNotifier.of(context);
        final routeAnimation = ModalRoute.of(context)?.animation ??
            const AlwaysStoppedAnimation(1.0);
        final dialog = AlertDialog(
          title: control.buildTextOrWidget("title"),
          titlePadding: control.getPadding("title_padding"),
          content: control.buildWidget("content"),
          contentPadding: control.getPadding("content_padding",
              const EdgeInsets.fromLTRB(24.0, 20.0, 24.0, 24.0))!,
          actions: control.buildWidgets("actions"),
          actionsPadding: control.getPadding("actions_padding"),
          actionsAlignment: control.getMainAxisAlignment("actions_alignment"),
          shape: control.getShape("shape", Theme.of(context)),
          semanticLabel: control.getString("semantics_label"),
          insetPadding: control.getPadding("inset_padding",
              const EdgeInsets.symmetric(horizontal: 40.0, vertical: 24.0))!,
          iconPadding: control.getPadding("icon_padding"),
          backgroundColor: control.getColor("bgcolor", context),
          buttonPadding: control.getPadding("action_button_padding"),
          shadowColor: control.getColor("shadow_color", context),
          elevation: control.getDouble("elevation"),
          clipBehavior:
              parseClip(control.getString("clip_behavior"), Clip.none)!,
          icon: control.buildIconOrWidget("icon"),
          iconColor: control.getColor("icon_color", context),
          scrollable: control.getBool("scrollable", false)!,
          actionsOverflowButtonSpacing:
              control.getDouble("actions_overflow_button_spacing"),
          alignment: control.getAlignment("alignment"),
          contentTextStyle:
              control.getTextStyle("content_text_style", Theme.of(context)),
          titleTextStyle:
              control.getTextStyle("title_text_style", Theme.of(context)),
        );
        return Stack(
          fit: StackFit.expand,
          children: [
            IgnorePointer(
              child: FadeTransition(
                opacity: routeAnimation,
                child: ColoredBox(
                  color: control.getColor("barrier_color", context) ??
                      DialogTheme.of(context).barrierColor ??
                      Theme.of(context).dialogTheme.barrierColor ??
                      Colors.black54,
                ),
              ),
            ),
            SafeArea(child: BaseControl(control: control, child: dialog)),
          ],
        );
      }),
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("AlertDialog build: ${control.id}");

    var open = control.getBool("open", false)!;
    final lastOpen = control.getBool("_open", false)!;
    var modal = control.getBool("modal", false)!;

    if (open && (open != lastOpen)) {
      if (control.get("title") == null &&
          control.get("content") == null &&
          control.children("actions").isEmpty) {
        return const ErrorControl(
            "AlertDialog has nothing to display. Provide at minimum one of the following: title, content, actions.");
      }

      control.updateProperties({"_open": open}, python: false);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog(
            barrierDismissible: !modal,
            // Render the barrier in the dialog widget so it updates live.
            barrierColor: Colors.transparent,
            useSafeArea: false,
            useRootNavigator: false,
            context: context,
            builder: (context) => _createAlertDialog(context)).then((value) {
          debugPrint("Dismissing AlertDialog(${control.id})");
          control.updateProperties({"_open": false}, python: false);
          control.updateProperties({"open": false});
          control.triggerEvent("dismiss");
        });
      });
    } else if (!open && lastOpen) {
      if (Navigator.of(context).canPop() == true) {
        debugPrint(
            "AlertDialog(${control.id}): Closing dialog managed by this widget.");
        Navigator.of(context).pop();
        control.updateProperties({"_open": false}, python: false);
      } else {
        debugPrint(
            "AlertDialog(${control.id}): Dialog was not opened by this widget, skipping pop.");
      }
    }
    return const SizedBox.shrink();
  }
}
