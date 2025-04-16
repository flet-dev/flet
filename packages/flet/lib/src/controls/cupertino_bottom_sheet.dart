import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';

class CupertinoBottomSheetControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final Widget? nextChild;
  final FletControlBackend backend;

  const CupertinoBottomSheetControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentAdaptive,
      required this.parentDisabled,
      required this.nextChild,
      required this.backend});

  @override
  State<CupertinoBottomSheetControl> createState() =>
      _CupertinoBottomSheetControlState();
}

class _CupertinoBottomSheetControlState
    extends State<CupertinoBottomSheetControl> {
  Widget _createDialog() {
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);

    Widget content = contentCtrls.isNotEmpty
        ? createControl(widget.control, contentCtrls.first.id, disabled,
            parentAdaptive: widget.parentAdaptive)
        : const SizedBox.shrink();

    if (contentCtrls.isNotEmpty &&
        ["cupertinopicker", "cupertinotimerpicker", "cupertinodatepicker"]
            .contains(contentCtrls.first.type)) {
      content = Container(
        height: widget.control.attrDouble("height", 220.0)!,
        padding: parseEdgeInsets(widget.control, "padding"),
        // bottom margin is provided to align the popup above the system navigation bar
        margin:
            EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
        // popup background color
        color: widget.control.attrColor("bgcolor", context,
            CupertinoColors.systemBackground.resolveFrom(context))!,
        // Use SafeArea to avoid system overlaps
        child: SafeArea(
          top: false,
          child: content,
        ),
      );
    }

    return Material(child: content);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoBottomSheet build: ${widget.control.id}");

    bool lastOpen = widget.control.state["open"] ?? false;

    var open = widget.control.attrBool("open", false)!;
    var modal = widget.control.attrBool("modal", false)!;

    debugPrint("Current open state: $lastOpen");
    debugPrint("New open state: $open");

    if (open && (open != lastOpen)) {
      var dialog = _createDialog();
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
            builder: (context) => _createDialog()).then((value) {
          lastOpen = widget.control.state["open"] ?? false;
          debugPrint(
              "CupertinoBottomSheet should be dismissed ($hashCode): $lastOpen");
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
