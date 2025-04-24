import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/dismissible.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';

class SnackBarControl extends StatefulWidget {
  final Control control;

  const SnackBarControl({
    super.key,
    required this.control,
  });

  @override
  State<SnackBarControl> createState() => _SnackBarControlState();
}

class _SnackBarControlState extends State<SnackBarControl> {
  Widget? _dialog;
  bool _open = false;
  bool _dismissed = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    debugPrint("SnackBar.didChangeDependencies: ${widget.control.id}");
    _toggleSnackBar();
  }

  @override
  void didUpdateWidget(covariant SnackBarControl oldWidget) {
    debugPrint("SnackBar.didUpdateWidget: ${widget.control.id}");
    super.didUpdateWidget(oldWidget);
    _toggleSnackBar();
  }

  Widget _createSnackBar(FletBackend backend) {
    if (widget.control.get("content") == null) {
      return const ErrorControl(
          "SnackBar.content must be provided and visible");
    }

    var actionName = widget.control.getString("action", "")!;
    SnackBarAction? action = actionName != "" // fixme
        ? SnackBarAction(
            label: actionName,
            textColor: widget.control.getColor("action_color", context),
            onPressed: () {
              widget.control.triggerEvent("action");
            })
        : null;

    SnackBarBehavior? behavior = widget.control.getSnackBarBehavior("behavior");

    var width = widget.control.getDouble("width");
    var margin = widget.control.getMargin("margin");

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
            widget.control.getString("clip_behavior"), Clip.hardEdge)!,
        actionOverflowThreshold:
            widget.control.getDouble("action_overflow_threshold"),
        shape: widget.control.getOutlinedBorder("shape", Theme.of(context)),
        onVisible: () {
          backend.triggerControlEvent(widget.control, "visible");
        },
        dismissDirection: parseDismissDirection(
            widget.control.getString("dismiss_direction")),
        showCloseIcon: widget.control.getBool("show_close_icon"),
        closeIconColor: widget.control.getColor("close_icon_color", context),
        content: widget.control.buildWidget("content")!,
        backgroundColor: widget.control.getColor("bgcolor", context),
        action: action,
        margin: margin,
        padding: widget.control.getPadding("padding"),
        width: width,
        elevation: widget.control.getDouble("elevation"),
        duration:
            Duration(milliseconds: widget.control.getInt("duration", 4000)!));
  }

  void _toggleSnackBar() {
    if (_dismissed) return;

    debugPrint("SnackBar build: ${widget.control.id}");

    var open = widget.control.getBool("open", false)!;

    if (open && (open != _open)) {
      _dialog = _createSnackBar(FletBackend.of(context));

      if (_dialog is ErrorControl) {
        debugPrint(
            "SnackBar: ErrorControl, not showing dialog: ${(_dialog as ErrorControl).message}");
        return;
      }

      _open = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        ScaffoldMessenger.of(context).removeCurrentSnackBar();
        ScaffoldMessenger.of(context)
            .showSnackBar(_dialog as SnackBar)
            .closed
            .then((reason) {
          if (!_dismissed) {
            _dismissed = true;
            debugPrint(
                "Dismissing SnackBar(${widget.control.id}) with reason: $reason");
            _open = false;
            widget.control.updateProperties({"open": false});
            widget.control.triggerEvent("dismiss");
          }
        });
      });
    } else if (!open && _open) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        ScaffoldMessenger.of(context).removeCurrentSnackBar();
        _open = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return _dialog is ErrorControl ? _dialog! : const SizedBox.shrink();
  }
}
