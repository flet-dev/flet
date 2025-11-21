import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/dismissible.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';
import '../widgets/error.dart';

class SnackBarControl extends StatelessWidget {
  final Control control;

  const SnackBarControl({super.key, required this.control});

  Widget _createSnackBar(BuildContext context) {
    var content = control.buildTextOrWidget("content");
    if (content == null) {
      return const ErrorControl(
          "SnackBar.content must be provided and visible");
    }

    var backend = FletBackend.of(context);

    final actionControl = control.get("action");
    SnackBarAction? action;
    if (actionControl is Control) {
      action = SnackBarAction(
        label: actionControl.getString("label", "Action")!,
        backgroundColor: actionControl.getColor("bgcolor", context),
        textColor: actionControl.getColor("text_color", context),
        disabledBackgroundColor:
            actionControl.getColor("disabled_bgcolor", context),
        disabledTextColor:
            actionControl.getColor("disabled_text_color", context),
        onPressed: () => actionControl.triggerEvent("click"),
      );
    } else if (actionControl is String) {
      action = SnackBarAction(
        label: actionControl,
        onPressed: () => control.triggerEvent("action"),
      );
    }

    var width = control.getDouble("width");
    var margin = control.getMargin("margin");

    // if behavior is not floating, ignore margin and width
    SnackBarBehavior? behavior = control.getSnackBarBehavior("behavior");
    if (behavior != SnackBarBehavior.floating) {
      margin = null;
      width = null;
    }

    // if width is provided, margin is ignored (both can't be used together)
    margin = (width != null && margin != null) ? null : margin;

    return SnackBar(
      behavior: behavior,
      clipBehavior: control.getClipBehavior("clip_behavior", Clip.hardEdge)!,
      actionOverflowThreshold: control.getDouble("action_overflow_threshold"),
      shape: control.getOutlinedBorder("shape", Theme.of(context)),
      onVisible: () {
        backend.triggerControlEvent(control, "visible");
      },
      dismissDirection: control.getDismissDirection("dismiss_direction"),
      showCloseIcon: control.getBool("show_close_icon"),
      closeIconColor: control.getColor("close_icon_color", context),
      content: content,
      backgroundColor: control.getColor("bgcolor", context),
      action: action,
      margin: margin,
      padding: control.getPadding("padding"),
      width: width,
      elevation: control.getDouble("elevation"),
      duration:
          control.getDuration("duration", const Duration(milliseconds: 4000))!,
    );
  }

  @override
  Widget build(BuildContext context) {
    final dismissed = control.getBool("_dismissed", false)!;

    if (!dismissed) {
      final open = control.getBool("open", false)!;
      final lastOpen = control.getBool("_open", false)!;

      debugPrint(
          "SnackBar build: ${control.id}, open: $open, _open: $lastOpen");

      if (open && (open != lastOpen)) {
        var dialog = _createSnackBar(context);

        if (dialog is ErrorControl) {
          debugPrint(
              "SnackBar: ErrorControl, not showing dialog: ${dialog.message}");
          return dialog;
        }

        control.updateProperties({"_open": open}, python: false);

        WidgetsBinding.instance.addPostFrameCallback((_) {
          ScaffoldMessenger.of(context).removeCurrentSnackBar();
          ScaffoldMessenger.of(context)
              .showSnackBar(dialog as SnackBar)
              .closed
              .then((reason) {
            if (!dismissed) {
              control.updateProperties({"_dismissed": true});
              debugPrint(
                  "Dismissing SnackBar(${control.id}) with reason: $reason");
              control.updateProperties({"_open": false}, python: false);
              control.updateProperties({"open": false});
              control.triggerEvent("dismiss");
            }
          });
        });
      } else if (!open && lastOpen) {
        WidgetsBinding.instance.addPostFrameCallback((_) {
          ScaffoldMessenger.of(context).removeCurrentSnackBar();
          control.updateProperties({"_open": false}, python: false);
        });
      }
    }
    return const SizedBox.shrink();
  }
}
