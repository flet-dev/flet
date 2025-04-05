import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
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
    var titleControl = widget.control.get("title");
    var contentWidget = widget.control.buildWidget("content");
    var actionWidgets = widget.control.buildWidgets("actions");
    if (titleControl == null &&
        contentWidget == null &&
        actionWidgets.isEmpty) {
      return const ErrorControl(
          "AlertDialog has nothing to display. Provide at minimum one of the following: title, content, actions");
    }

    final actionsAlignment =
        parseMainAxisAlignment(widget.control.getString("actionsAlignment"));
    var clipBehavior =
        parseClip(widget.control.getString("clipBehavior"), Clip.none)!;

    return AlertDialog(
      title: titleControl is Control
          ? ControlWidget(control: titleControl)
          : titleControl is String
              ? Text(titleControl)
              : null,
      titlePadding: parseEdgeInsets(widget.control, "title_padding"),
      content: contentWidget,
      contentPadding: parseEdgeInsets(widget.control, "content_padding",
          const EdgeInsets.fromLTRB(24.0, 20.0, 24.0, 24.0))!,
      actions: actionWidgets,
      actionsPadding: parseEdgeInsets(widget.control, "actions_padding"),
      actionsAlignment: actionsAlignment,
      shape: parseOutlinedBorder(widget.control, "shape"),
      semanticLabel: widget.control.getString("semantics_label"),
      insetPadding: parseEdgeInsets(widget.control, "inset_padding",
          const EdgeInsets.symmetric(horizontal: 40.0, vertical: 24.0))!,
      iconPadding: parseEdgeInsets(widget.control, "icon_padding"),
      backgroundColor: widget.control.getColor("bgcolor", context),
      buttonPadding: parseEdgeInsets(widget.control, "action_button_padding"),
      surfaceTintColor: widget.control.getColor("surface_tint_color", context),
      shadowColor: widget.control.getColor("shadow_color", context),
      elevation: widget.control.getDouble("elevation"),
      clipBehavior: clipBehavior,
      icon: widget.control.buildWidget("icon"),
      iconColor: widget.control.getColor("icon_color", context),
      scrollable: widget.control.getBool("scrollable", false)!,
      actionsOverflowButtonSpacing:
          widget.control.getDouble("actions_overflow_button_spacing"),
      alignment: parseAlignment(widget.control, "alignment"),
      contentTextStyle: parseTextStyle(
          Theme.of(context), widget.control, "content_text_style"),
      titleTextStyle:
          parseTextStyle(Theme.of(context), widget.control, "title_text_style"),
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
            builder: (context) => _createAlertDialog()).then((value) {
          if (_open) {
            debugPrint("Dismissing AlertDialog(${widget.control.id})");
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
