import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class CupertinoActionSheetControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final Widget? nextChild;
  final FletControlBackend backend;

  const CupertinoActionSheetControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.nextChild,
      required this.backend});

  @override
  State<CupertinoActionSheetControl> createState() =>
      _CupertinoActionSheetControlState();
}

class _CupertinoActionSheetControlState
    extends State<CupertinoActionSheetControl> {
  Widget _createActionSheet() {
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var titleCtrls =
        widget.children.where((c) => c.name == "title" && c.isVisible);
    var messageCtrls =
        widget.children.where((c) => c.name == "message" && c.isVisible);
    var cancelButtonCtrls =
        widget.children.where((c) => c.name == "cancel" && c.isVisible);
    var actionCtrls =
        widget.children.where((c) => c.name == "action" && c.isVisible);

    return CupertinoActionSheet(
      title: titleCtrls.isNotEmpty
          ? createControl(widget.control, titleCtrls.first.id, disabled,
              parentAdaptive: widget.parentAdaptive)
          : null,
      message: messageCtrls.isNotEmpty
          ? createControl(widget.control, messageCtrls.first.id, disabled,
              parentAdaptive: widget.parentAdaptive)
          : null,
      cancelButton: cancelButtonCtrls.isNotEmpty
          ? createControl(widget.control, cancelButtonCtrls.first.id, disabled,
              parentAdaptive: widget.parentAdaptive)
          : null,
      actions: actionCtrls.isNotEmpty
          ? actionCtrls
              .map((c) => createControl(widget.control, c.id, disabled,
                  parentAdaptive: widget.parentAdaptive))
              .toList()
          : null,
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoActionSheetControl build: ${widget.control.id}");

    bool lastOpen = widget.control.state["open"] ?? false;

    var open = widget.control.attrBool("open", false)!;
    var modal = widget.control.attrBool("modal", false)!;

    debugPrint("Current open state: $lastOpen");
    debugPrint("New open state: $open");

    if (open && (open != lastOpen)) {
      var dialog = _createActionSheet();
      if (dialog is ErrorControl) {
        return dialog;
      }

      // close previous dialog
      if (ModalRoute.of(context)?.isCurrent != true) {
        Navigator.of(context).pop();
      }

      widget.control.state["open"] = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showCupertinoModalPopup(
            barrierDismissible: !modal,
            useRootNavigator: false,
            context: context,
            builder: (context) => _createActionSheet()).then((value) {
          lastOpen = widget.control.state["open"] ?? false;
          debugPrint("Action sheet should be dismissed ($hashCode): $lastOpen");
          bool shouldDismiss = lastOpen;
          widget.control.state["open"] = false;

          if (shouldDismiss) {
            widget.backend
                .updateControlState(widget.control.id, {"open": "false"});
            widget.backend
                .triggerControlEvent(widget.control.id, "dismiss", "");
          }
        });
      });
    } else if (open != lastOpen && lastOpen) {
      Navigator.of(context).pop();
    }

    return widget.nextChild ?? const SizedBox.shrink();
  }
}
