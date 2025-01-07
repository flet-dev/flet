import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import 'create_control.dart';
import 'error.dart';

class CupertinoAlertDialogControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final Widget? nextChild;
  final FletControlBackend backend;

  const CupertinoAlertDialogControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.nextChild,
      required this.backend});

  @override
  State<CupertinoAlertDialogControl> createState() =>
      _CupertinoAlertDialogControlState();
}

class _CupertinoAlertDialogControlState
    extends State<CupertinoAlertDialogControl> {
  Widget _createCupertinoAlertDialog() {
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var titleCtrls =
        widget.children.where((c) => c.name == "title" && c.isVisible);
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    var actionCtrls =
        widget.children.where((c) => c.name == "action" && c.isVisible);
    if (titleCtrls.isEmpty && contentCtrls.isEmpty && actionCtrls.isEmpty) {
      return const ErrorControl(
          "CupertinoAlertDialog has nothing to display. Provide at minimum one of the following: title, content, actions");
    }
    var insetAnimation = parseAnimation(
        widget.control,
        "insetAnimation",
        ImplicitAnimationDetails(
            duration: const Duration(milliseconds: 100),
            curve: Curves.decelerate))!;

    return CupertinoAlertDialog(
      insetAnimationCurve: insetAnimation.curve,
      insetAnimationDuration: insetAnimation.duration,
      title: titleCtrls.isNotEmpty
          ? createControl(widget.control, titleCtrls.first.id, disabled,
              parentAdaptive: widget.parentAdaptive)
          : null,
      content: contentCtrls.isNotEmpty
          ? createControl(widget.control, contentCtrls.first.id, disabled,
              parentAdaptive: widget.parentAdaptive)
          : null,
      actions: actionCtrls
          .map((c) => createControl(widget.control, c.id, disabled,
              parentAdaptive: widget.parentAdaptive))
          .toList(),
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoAlertDialog build ($hashCode): ${widget.control.id}");

    bool lastOpen = widget.control.state["open"] ?? false;

    debugPrint("CupertinoAlertDialog build: ${widget.control.id}");

    var open = widget.control.attrBool("open", false)!;
    var modal = widget.control.attrBool("modal", false)!;

    debugPrint("Current open state: $lastOpen");
    debugPrint("New open state: $open");

    if (open && (open != lastOpen)) {
      var dialog = _createCupertinoAlertDialog();
      if (dialog is ErrorControl) {
        return dialog;
      }

      // close previous dialog
      if (ModalRoute.of(context)?.isCurrent != true) {
        Navigator.of(context).pop();
      }

      widget.control.state["open"] = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog(
            barrierDismissible: !modal,
            barrierColor: widget.control.attrColor("barrierColor", context),
            useRootNavigator: false,
            context: context,
            builder: (context) => dialog).then((value) {
          lastOpen = widget.control.state["open"] ?? false;
          debugPrint("Dialog should be dismissed ($hashCode): $lastOpen");
          bool shouldDismiss = lastOpen;
          widget.control.state["open"] = false;

          if (shouldDismiss) {
            widget.backend
                .updateControlState(widget.control.id, {"open": "false"});
            widget.backend.triggerControlEvent(widget.control.id, "dismiss");
          }
        });
      });
    } else if (open != lastOpen && lastOpen) {
      Navigator.of(context).pop();
    }

    return widget.nextChild ?? const SizedBox.shrink();
  }
}
