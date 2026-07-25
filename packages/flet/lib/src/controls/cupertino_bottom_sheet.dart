import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../controls/control_widget.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';

class CupertinoBottomSheetControl extends StatefulWidget {
  final Control control;

  const CupertinoBottomSheetControl({
    super.key,
    required this.control,
  });

  @override
  State<CupertinoBottomSheetControl> createState() =>
      _CupertinoBottomSheetControlState();
}

class _CupertinoBottomSheetControlState
    extends State<CupertinoBottomSheetControl> {
  // The modal route this control pushed, tracked so the close path can pop
  // exactly this route (never whatever happens to be topmost) after the frame.
  ModalRoute? _popupRoute;

  Widget _createDialog(BuildContext context) {
    final control = widget.control;
    Control? content = control.child("content");

    if (content == null) {
      return const ErrorControl("CupertinoBottomSheet.content is empty.");
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
    final control = widget.control;
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
        if (!context.mounted) return;
        showCupertinoModalPopup(
            barrierDismissible: !control.getBool("modal", false)!,
            useRootNavigator: false,
            context: context,
            builder: (context) {
              _popupRoute = ModalRoute.of(context);
              return dialog;
            }).then((value) {
          (_popupRoute?.completed ?? Future.value()).then((_) {
            _popupRoute = null;
            control.updateProperties({"_open": false}, python: false);
            control.updateProperties({"open": false});
            control.triggerEvent("dismiss");
          });
        });
      });
    } else if (open != lastOpen && lastOpen) {
      // Mark closed now so this branch doesn't re-fire, then close after the
      // frame. Popping during build throws "setState() called during build"
      // when the same frame also opens another route/overlay (e.g. a SnackBar).
      control.updateProperties({"_open": open}, python: false);
      final route = _popupRoute;
      _popupRoute = null;
      if (route != null) {
        WidgetsBinding.instance.addPostFrameCallback((_) {
          closeModalRoute(route);
        });
      }
    }

    return const SizedBox.shrink();
  }
}
