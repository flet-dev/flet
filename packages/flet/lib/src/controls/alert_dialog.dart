import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../widgets/error.dart';
import 'control_widget.dart';

class AlertDialogControl extends StatefulWidget {
  final Control control;

  const AlertDialogControl({super.key, required this.control});

  @override
  State<AlertDialogControl> createState() => _AlertDialogControlState();
}

class _AlertDialogControlState extends State<AlertDialogControl> {
  Widget? _dialog;
  bool _open = false;
  NavigatorState? _navigatorState;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    debugPrint("AlertDialog.didChangeDependencies: ${widget.control.id}");
    _navigatorState = Navigator.of(context);
    _toggleDialog();
  }

  @override
  void didUpdateWidget(covariant AlertDialogControl oldWidget) {
    debugPrint("AlertDialog.didUpdateWidget: ${widget.control.id}");
    super.didUpdateWidget(oldWidget);
    _toggleDialog();
  }

  @override
  void dispose() {
    debugPrint("AlertDialog.dispose: ${widget.control.id}");
    _closeDialog();
    super.dispose();
  }

  Widget _createAlertDialog() {
    var title = widget.control.get("title");
    var content = widget.control.buildWidget("content");
    var actions = widget.control.buildWidgets("actions");
    if (title == null && content == null && actions.isEmpty) {
      return const ErrorControl(
          "AlertDialog has nothing to display. Provide at minimum one of the following: title, content, actions");
    }

    final actionsAlignment =
        widget.control.getMainAxisAlignment("actionsAlignment");
    var clipBehavior =
        parseClip(widget.control.getString("clipBehavior"), Clip.none)!;

    return AlertDialog(
      title: title is Control
          ? ControlWidget(control: title)
          : title is String
              ? Text(title)
              : null,
      titlePadding: widget.control.getPadding("title_padding"),
      content: content,
      contentPadding: widget.control.getPadding("content_padding",
          const EdgeInsets.fromLTRB(24.0, 20.0, 24.0, 24.0))!,
      actions: actions,
      actionsPadding: widget.control.getPadding("actions_padding"),
      actionsAlignment: actionsAlignment,
      shape: widget.control.getShape("shape"),
      semanticLabel: widget.control.getString("semantics_label"),
      insetPadding: widget.control.getPadding("inset_padding",
          const EdgeInsets.symmetric(horizontal: 40.0, vertical: 24.0))!,
      iconPadding: widget.control.getPadding("icon_padding"),
      backgroundColor: widget.control.getColor("bgcolor", context),
      buttonPadding: widget.control.getPadding("action_button_padding"),
      surfaceTintColor: widget.control.getColor("surface_tint_color", context),
      shadowColor: widget.control.getColor("shadow_color", context),
      elevation: widget.control.getDouble("elevation"),
      clipBehavior: clipBehavior,
      icon: widget.control.buildWidget("icon"),
      iconColor: widget.control.getColor("icon_color", context),
      scrollable: widget.control.getBool("scrollable", false)!,
      actionsOverflowButtonSpacing:
          widget.control.getDouble("actions_overflow_button_spacing"),
      alignment: widget.control.getAlignment("alignment"),
      contentTextStyle:
          widget.control.getTextStyle("content_text_style", Theme.of(context)),
      titleTextStyle:
          widget.control.getTextStyle("title_text_style", Theme.of(context)),
    );
  }

  void _toggleDialog() {
    debugPrint("AlertDialog build: ${widget.control.id}");

    var open = widget.control.getBool("open", false)!;
    var modal = widget.control.getBool("modal", false)!;

    if (open && (open != _open)) {
      _dialog = _createAlertDialog();

      if (_dialog is ErrorControl) {
        debugPrint(
            "AlertDialog: ErrorControl, not showing dialog: ${(_dialog as ErrorControl).message}");
        return;
      }

      _open = open;

      var backend = FletBackend.of(context);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog(
            barrierDismissible: !modal,
            barrierColor: widget.control.getColor("barrierColor", context),
            useRootNavigator: false,
            context: context,
            builder: (context) => _dialog!).then((value) {
          debugPrint("Dismissing AlertDialog(${widget.control.id})");
          _open = false;
          backend.updateControl(widget.control.id, {"open": false});
          backend.triggerControlEvent(widget.control, "dismiss");
        });
      });
    } else if (!open && _open) {
      _closeDialog();
    }
  }

  @override
  Widget build(BuildContext context) {
    return _dialog is ErrorControl ? _dialog! : const SizedBox.shrink();
  }

  void _closeDialog() {
    if (_open) {
      if (_navigatorState?.canPop() == true) {
        debugPrint(
            "AlertDialog(${widget.control.id}): Closing dialog managed by this widget.");
        _navigatorState?.pop();
        _open = false;
        _dialog = null;
      } else {
        debugPrint(
            "AlertDialog(${widget.control.id}): Dialog was not opened by this widget, skipping pop.");
      }
    }
  }
}
