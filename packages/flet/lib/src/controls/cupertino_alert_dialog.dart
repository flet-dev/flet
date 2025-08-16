import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../widgets/control_inherited_notifier.dart';
import '../widgets/error.dart';

class CupertinoAlertDialogControl extends StatefulWidget {
  final Control control;

  CupertinoAlertDialogControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<CupertinoAlertDialogControl> createState() =>
      _CupertinoAlertDialogControlState();
}

class _CupertinoAlertDialogControlState
    extends State<CupertinoAlertDialogControl> {
  bool _open = false;
  NavigatorState? _navigatorState;
  String? _error;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    debugPrint(
        "CupertinoAlertDialog.didChangeDependencies: ${widget.control.id}");
    _navigatorState = Navigator.of(context);
    _toggleDialog();
  }

  @override
  void didUpdateWidget(covariant CupertinoAlertDialogControl oldWidget) {
    debugPrint("CupertinoAlertDialog.didUpdateWidget: ${widget.control.id}");
    super.didUpdateWidget(oldWidget);
    _toggleDialog();
  }

  @override
  void dispose() {
    debugPrint("CupertinoAlertDialog.dispose: ${widget.control.id}");
    _closeDialog();
    super.dispose();
  }

  Widget _createCupertinoAlertDialog() {
    return ControlInheritedNotifier(
      notifier: widget.control,
      child: Builder(builder: (context) {
        ControlInheritedNotifier.of(context);
        var insetAnimation = parseAnimation(
            widget.control.get("inset_animation"),
            ImplicitAnimationDetails(
                duration: const Duration(milliseconds: 100),
                curve: Curves.decelerate))!;

        return CupertinoAlertDialog(
          insetAnimationCurve: insetAnimation.curve,
          insetAnimationDuration: insetAnimation.duration,
          title: widget.control.buildTextOrWidget("title"),
          content: widget.control.buildWidget("content"),
          actions: widget.control.buildWidgets("actions"),
        );
      }),
    );
  }

  void _toggleDialog() {
    debugPrint("CupertinoAlertDialog build: ${widget.control.id}");

    var open = widget.control.getBool("open", false)!;
    var modal = widget.control.getBool("modal", false)!;

    if (open && (open != _open)) {
      if (widget.control.get("title") == null &&
          widget.control.get("content") == null &&
          widget.control.children("actions").isEmpty) {
        _error =
            "CupertinoAlertDialog has nothing to display. Provide at minimum one of the following: title, content, actions.";
        return;
      }

      _open = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog(
            barrierDismissible: !modal,
            barrierColor: widget.control.getColor("barrier_color", context),
            useRootNavigator: false,
            context: context,
            builder: (context) => _createCupertinoAlertDialog()).then((value) {
          debugPrint("Dismissing CupertinoAlertDialog(${widget.control.id})");
          _open = false;
          widget.control.updateProperties({"open": false});
          widget.control.triggerEvent("dismiss");
        });
      });
    } else if (!open && _open) {
      _closeDialog();
    }
  }

  void _closeDialog() {
    if (_open) {
      if (_navigatorState?.canPop() == true) {
        debugPrint(
            "CupertinoAlertDialog(${widget.control.id}): Closing dialog managed by this widget.");
        _navigatorState?.pop();
        _open = false;
        _error = null;
      } else {
        debugPrint(
            "CupertinoAlertDialog(${widget.control.id}): Dialog was not opened by this widget, skipping pop.");
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return _error != null ? ErrorControl(_error!) : const SizedBox.shrink();
  }
}
