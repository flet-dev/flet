import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';

class CupertinoAlertDialogControl extends StatefulWidget {
  final Control control;

  CupertinoAlertDialogControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<CupertinoAlertDialogControl> createState() =>
      _CupertinoAlertDialogControlState();
}

class _CupertinoAlertDialogControlState
    extends State<CupertinoAlertDialogControl> {
  Widget? _dialog;
  bool _open = false;
  NavigatorState? _navigatorState;

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
    var title = widget.control.buildTextOrWidget("title");
    var content = widget.control.buildWidget("content");
    var actions = widget.control.buildWidgets("actions");
    if (title == null && content == null && actions.isEmpty) {
      return const ErrorControl(
          "CupertinoAlertDialog has nothing to display. Provide at minimum one of the following: title, content, actions");
    }
    var insetAnimation = parseAnimation(
        widget.control.get("inset_animation"),
        ImplicitAnimationDetails(
            duration: const Duration(milliseconds: 100),
            curve: Curves.decelerate))!;

    return CupertinoAlertDialog(
      insetAnimationCurve: insetAnimation.curve,
      insetAnimationDuration: insetAnimation.duration,
      title: title,
      content: content,
      actions: actions,
    );
  }

  void _toggleDialog() {
    debugPrint("CupertinoAlertDialog build: ${widget.control.id}");

    var open = widget.control.getBool("open", false)!;
    var modal = widget.control.getBool("modal", false)!;

    if (open && (open != _open)) {
      _dialog = _createCupertinoAlertDialog();

      if (_dialog is ErrorControl) {
        debugPrint(
            "CupertinoAlertDialog: ErrorControl, not showing dialog: ${(_dialog as ErrorControl).message}");
        return;
      }

      _open = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog(
            barrierDismissible: !modal,
            barrierColor: widget.control.getColor("barrier_color", context),
            useRootNavigator: false,
            context: context,
            builder: (context) => _dialog!).then((value) {
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
        _dialog = null;
      } else {
        debugPrint(
            "CupertinoAlertDialog(${widget.control.id}): Dialog was not opened by this widget, skipping pop.");
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return _dialog is ErrorControl ? _dialog! : const SizedBox.shrink();
  }
}
