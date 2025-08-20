import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../widgets/control_inherited_notifier.dart';
import '../widgets/error.dart';
import 'control_widget.dart';

class AlertDialogControl extends StatefulWidget {
  final Control control;

  AlertDialogControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<AlertDialogControl> createState() => _AlertDialogControlState();
}

class _AlertDialogControlState extends State<AlertDialogControl> {
  bool _open = false;
  NavigatorState? _navigatorState;
  String? _error;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _navigatorState = Navigator.of(context);
    _toggleDialog();
  }

  @override
  void didUpdateWidget(covariant AlertDialogControl oldWidget) {
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
    return ControlInheritedNotifier(
      notifier: widget.control,
      child: Builder(builder: (context) {
        ControlInheritedNotifier.of(context);
        var title = widget.control.get("title");
        return AlertDialog(
          title: title is Control
              ? ControlWidget(control: title)
              : title is String
                  ? Text(title)
                  : null,
          titlePadding: widget.control.getPadding("title_padding"),
          content: widget.control.buildWidget("content"),
          contentPadding: widget.control.getPadding("content_padding",
              const EdgeInsets.fromLTRB(24.0, 20.0, 24.0, 24.0))!,
          actions: widget.control.buildWidgets("actions"),
          actionsPadding: widget.control.getPadding("actions_padding"),
          actionsAlignment:
              widget.control.getMainAxisAlignment("actions_alignment"),
          shape: widget.control.getShape("shape", Theme.of(context)),
          semanticLabel: widget.control.getString("semantics_label"),
          insetPadding: widget.control.getPadding("inset_padding",
              const EdgeInsets.symmetric(horizontal: 40.0, vertical: 24.0))!,
          iconPadding: widget.control.getPadding("icon_padding"),
          backgroundColor: widget.control.getColor("bgcolor", context),
          buttonPadding: widget.control.getPadding("action_button_padding"),
          shadowColor: widget.control.getColor("shadow_color", context),
          elevation: widget.control.getDouble("elevation"),
          clipBehavior:
              parseClip(widget.control.getString("clip_behavior"), Clip.none)!,
          icon: widget.control.buildIconOrWidget("icon"),
          iconColor: widget.control.getColor("icon_color", context),
          scrollable: widget.control.getBool("scrollable", false)!,
          actionsOverflowButtonSpacing:
              widget.control.getDouble("actions_overflow_button_spacing"),
          alignment: widget.control.getAlignment("alignment"),
          contentTextStyle: widget.control
              .getTextStyle("content_text_style", Theme.of(context)),
          titleTextStyle: widget.control
              .getTextStyle("title_text_style", Theme.of(context)),
        );
      }),
    );
  }

  void _toggleDialog() {
    debugPrint("AlertDialog build: ${widget.control.id}");

    var open = widget.control.getBool("open", false)!;
    var modal = widget.control.getBool("modal", false)!;

    if (open && (open != _open)) {
      if (widget.control.get("title") == null &&
          widget.control.get("content") == null &&
          widget.control.children("actions").isEmpty) {
        _error =
            "AlertDialog has nothing to display. Provide at minimum one of the following: title, content, actions.";
        return;
      }

      _open = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog(
            barrierDismissible: !modal,
            barrierColor: widget.control.getColor("barrier_color", context),
            useRootNavigator: false,
            context: context,
            builder: (context) => _createAlertDialog()).then((value) {
          debugPrint("Dismissing AlertDialog(${widget.control.id})");
          _open = false;
          widget.control.updateProperties({"open": false});
          widget.control.triggerEvent("dismiss");
        });
      });
    } else if (!open && _open) {
      _closeDialog();
    }
  }

  @override
  Widget build(BuildContext context) {
    return _error != null ? ErrorControl(_error!) : const SizedBox.shrink();
  }

  void _closeDialog() {
    if (_open) {
      if (_navigatorState?.canPop() == true) {
        debugPrint(
            "AlertDialog(${widget.control.id}): Closing dialog managed by this widget.");
        _navigatorState?.pop();
        _open = false;
        _error = null;
      } else {
        debugPrint(
            "AlertDialog(${widget.control.id}): Dialog was not opened by this widget, skipping pop.");
      }
    }
  }
}
