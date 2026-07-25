import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/colors.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../widgets/control_inherited_notifier.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class CupertinoAlertDialogControl extends StatefulWidget {
  final Control control;

  const CupertinoAlertDialogControl({super.key, required this.control});

  @override
  State<CupertinoAlertDialogControl> createState() =>
      _CupertinoAlertDialogControlState();
}

class _CupertinoAlertDialogControlState
    extends State<CupertinoAlertDialogControl> {
  // The dialog's own route, tracked so the close path can pop exactly this
  // route (never whatever is topmost) after the frame.
  ModalRoute? _dialogRoute;

  Widget _createCupertinoAlertDialog() {
    final control = widget.control;
    return ControlInheritedNotifier(
      notifier: control,
      child: Builder(builder: (context) {
        ControlInheritedNotifier.of(context);
        final routeAnimation = ModalRoute.of(context)?.animation ??
            const AlwaysStoppedAnimation(1.0);
        var insetAnimation = parseAnimation(
            control.get("inset_animation"),
            ImplicitAnimationDetails(
                duration: const Duration(milliseconds: 100),
                curve: Curves.decelerate))!;

        final dialog = CupertinoAlertDialog(
          insetAnimationCurve: insetAnimation.curve,
          insetAnimationDuration: insetAnimation.duration,
          title: control.buildTextOrWidget("title"),
          content: control.buildWidget("content"),
          actions: control.buildWidgets("actions"),
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
    final control = widget.control;
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
        if (!context.mounted) return;
        showDialog(
            barrierDismissible: !modal,
            // Render the barrier in the dialog widget so it updates live.
            barrierColor: Colors.transparent,
            useSafeArea: false,
            useRootNavigator: false,
            context: context,
            builder: (context) {
              _dialogRoute = ModalRoute.of(context);
              return _createCupertinoAlertDialog();
            }).then((value) {
          (_dialogRoute?.completed ?? Future.value()).then((_) {
            debugPrint("Dismissing CupertinoAlertDialog(${control.id})");
            _dialogRoute = null;
            control.updateProperties({"_open": false}, python: false);
            control.updateProperties({"open": false});
            control.triggerEvent("dismiss");
          });
        });
      });
    } else if (!open && lastOpen) {
      // Mark closed now so this branch doesn't re-fire, then close this
      // dialog's own route after the frame — popping during build throws
      // "setState() called during build" when the same frame opens another
      // route/overlay. Targeting `_dialogRoute` avoids racing `View`'s
      // confirm-pop, which also pops its own route.
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
