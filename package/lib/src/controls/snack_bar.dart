import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';

class SnackBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final Widget? nextChild;
  final FletControlBackend backend;

  const SnackBarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.nextChild,
      required this.backend});

  @override
  State<SnackBarControl> createState() => _SnackBarControlState();
}

class _SnackBarControlState extends State<SnackBarControl> {
  bool _open = false;

  Widget _createSnackBar() {
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var contentCtrls = widget.children.where((c) => c.name == "content");

    if (contentCtrls.isEmpty) {
      return const ErrorControl("SnackBar does not have a content.");
    }

    var actionName = widget.control.attrString("action", "")!;
    SnackBarAction? action = actionName != ""
        ? SnackBarAction(
            label: actionName,
            textColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("actionColor", "")!),
            onPressed: () {
              debugPrint("SnackBar ${widget.control.id} clicked!");
              widget.backend
                  .triggerControlEvent(widget.control.id, "action", "");
            })
        : null;

    SnackBarBehavior? behavior = SnackBarBehavior.values.firstWhereOrNull((a) =>
        a.name.toLowerCase() ==
        widget.control.attrString("behavior", "")!.toLowerCase());

    DismissDirection? dismissDirection = DismissDirection.values.firstWhere(
        (a) =>
            a.name.toLowerCase() ==
            widget.control.attrString("dismissDirection", "")!.toLowerCase(),
        orElse: () => DismissDirection.down);

    return SnackBar(
        behavior: behavior,
        dismissDirection: dismissDirection,
        showCloseIcon: widget.control.attrBool("showCloseIcon"),
        closeIconColor: HexColor.fromString(Theme.of(context),
            widget.control.attrString("closeIconColor", "")!),
        content: createControl(widget.control, contentCtrls.first.id, disabled,
            parentAdaptive: widget.parentAdaptive),
        backgroundColor: HexColor.fromString(
            Theme.of(context), widget.control.attrString("bgColor", "")!),
        action: action,
        margin: parseEdgeInsets(widget.control, "margin"),
        padding: parseEdgeInsets(widget.control, "padding"),
        width: widget.control.attrDouble("width"),
        elevation: widget.control.attrDouble("elevation"),
        duration:
            Duration(milliseconds: widget.control.attrInt("duration", 4000)!));
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SnackBar build: ${widget.control.id}");

    debugPrint("SnackBar build: ${widget.control.id}");

    var open = widget.control.attrBool("open", false)!;
    var removeCurrentSnackbar = true;

    //widget.control.attrBool("removeCurrentSnackBar", false)!;

    debugPrint("Current open state: $_open");
    debugPrint("New open state: $open");

    if (open && (open != _open)) {
      var snackBar = _createSnackBar();
      if (snackBar is ErrorControl) {
        return snackBar;
      }

      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (removeCurrentSnackbar) {
          ScaffoldMessenger.of(context).removeCurrentSnackBar();
        }
        ScaffoldMessenger.of(context).showSnackBar(snackBar as SnackBar);

        widget.backend.updateControlState(widget.control.id, {"open": "false"});
      });
    }

    _open = open;

    return widget.nextChild ?? const SizedBox.shrink();
  }
}
