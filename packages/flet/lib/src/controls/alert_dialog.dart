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

class AlertDialogControl extends StatefulWidget {
  final Control control;

  const AlertDialogControl({super.key, required this.control});

  @override
  State<AlertDialogControl> createState() => _AlertDialogControlState();
}

class _AlertDialogControlState extends State<AlertDialogControl> {
  // Route this widget pushed via `showDialog`.  Kept as state so the
  // dismiss path can pop *this* dialog specifically (via removeRoute)
  // instead of relying on `Navigator.pop()` which targets the topmost
  // route — that breaks when a sibling `use_dialog` host has already
  // appended a newer dialog above ours.
  ModalRoute? _dialogRoute;

  Control get control => widget.control;

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
          clipBehavior: control.getClipBehavior("clip_behavior", Clip.none)!,
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
            builder: (context) {
              _dialogRoute ??= ModalRoute.of(context);
              return _createAlertDialog(context);
            }).then((value) {
          final route = _dialogRoute;
          _dialogRoute = null;
          // showDialog future completes on pop() — before the exit animation
          // finishes.  Wait for the route's transition to fully complete so
          // the dismiss event fires after the closing animation ends.
          (route?.completed ?? Future.value()).then((_) {
            debugPrint("Dismissing AlertDialog(${control.id})");
            control.updateProperties({"_open": false}, python: false);
            control.updateProperties({"open": false});
            control.triggerEvent("dismiss");
          });
        });
      });
    } else if (!open && lastOpen) {
      // Mark closed now so this branch doesn't re-fire, then close this
      // dialog's own route after the frame. Popping during build throws
      // "setState() called during build" when the same frame opens another
      // route/overlay (e.g. a SnackBar). Targeting `_dialogRoute` (not the
      // topmost route) keeps this from racing `View`'s confirm-pop, which now
      // also pops its own route — see `test_pop_view_confirm`. `_dialogRoute`
      // is left set so the open path's `.then` still fires `dismiss` after the
      // close animation completes.
      control.updateProperties({"_open": false}, python: false);
      final route = _dialogRoute;
      if (route != null) {
        WidgetsBinding.instance.addPostFrameCallback((_) {
          closeModalRoute(route);
        });
      }
    }
    return const SizedBox.shrink();
  }
}
