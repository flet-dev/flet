import 'package:flet/src/flet_backend.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/animations.dart';
import '../widgets/error.dart';
import 'control_widget.dart';

class CupertinoAlertDialogControl extends StatefulWidget {
  final Control control;

  const CupertinoAlertDialogControl({super.key, required this.control});

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
    var titleControl = widget.control.child("title");
    var contentControl = widget.control.child("content");
    var actionControls = widget.control.children("actions");
    if (titleControl == null &&
        contentControl == null &&
        actionControls.isEmpty) {
      return const ErrorControl(
          "CupertinoAlertDialog has nothing to display. Provide at minimum one of the following: title, content, actions");
    }
    var insetAnimation = parseAnimation(
        widget.control,
        "inset_animation",
        ImplicitAnimationDetails(
            duration: const Duration(milliseconds: 100),
            curve: Curves.decelerate))!;

    return CupertinoAlertDialog(
      insetAnimationCurve: insetAnimation.curve,
      insetAnimationDuration: insetAnimation.duration,
      title: titleControl != null
          ? ControlWidget(
              control: titleControl,
            )
          : null,
      content: contentControl != null
          ? ControlWidget(
              control: contentControl,
            )
          : null,
      actions: actionControls
          .map((actionControl) => ControlWidget(
                control: actionControl,
              ))
          .toList(),
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

      var backend = FletBackend.of(context);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog(
            barrierDismissible: !modal,
            barrierColor: widget.control.getColor("barrier_color", context),
            useRootNavigator: false,
            context: context,
            builder: (context) => _dialog!).then((value) {
          if (_open) {
            debugPrint("Dismissing CupertinoAlertDialog(${widget.control.id})");
            _open = false;
            backend.updateControl(widget.control.id, {"open": false});
            backend.triggerControlEvent(widget.control, "dismiss");
          }
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
