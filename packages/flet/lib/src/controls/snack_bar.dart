import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/dismissible.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
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
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);

    if (contentCtrls.isEmpty) {
      return const ErrorControl(
          "SnackBar.content must be provided and visible");
    }

    var actionName = widget.control.attrString("action", "")!;
    SnackBarAction? action = actionName != ""
        ? SnackBarAction(
            label: actionName,
            textColor: widget.control.attrColor("actionColor", context),
            onPressed: () {
              debugPrint("SnackBar ${widget.control.id} clicked!");
              widget.backend.triggerControlEvent(widget.control.id, "action");
            })
        : null;

    SnackBarBehavior? behavior =
        parseSnackBarBehavior(widget.control.attrString("behavior"));

    var width = widget.control.attrDouble("width");
    var margin = parseEdgeInsets(widget.control, "margin");

    // if behavior is not floating, ignore margin and width
    if (behavior != SnackBarBehavior.floating) {
      margin = null;
      width = null;
    }

    // if width is provided, margin is ignored (both can't be used together)
    margin = (width != null && margin != null) ? null : margin;

    return SnackBar(
        behavior: behavior,
        clipBehavior: parseClip(
            widget.control.attrString("clipBehavior"), Clip.hardEdge)!,
        actionOverflowThreshold:
            widget.control.attrDouble("actionOverflowThreshold"),
        shape: parseOutlinedBorder(widget.control, "shape"),
        onVisible: () {
          debugPrint("SnackBar.onVisible(${widget.control.id})");
          widget.backend.triggerControlEvent(widget.control.id, "visible");
        },
        dismissDirection: parseDismissDirection(
            widget.control.attrString("dismissDirection")),
        showCloseIcon: widget.control.attrBool("showCloseIcon"),
        closeIconColor: widget.control.attrColor("closeIconColor", context),
        content: createControl(widget.control, contentCtrls.first.id, disabled,
            parentAdaptive: widget.parentAdaptive),
        backgroundColor: widget.control.attrColor("bgColor", context),
        action: action,
        margin: margin,
        padding: parseEdgeInsets(widget.control, "padding"),
        width: width,
        elevation: widget.control.attrDouble("elevation"),
        duration:
            Duration(milliseconds: widget.control.attrInt("duration", 4000)!));
  }

  @override
  Widget build(BuildContext context) {
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
