import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';

class CupertinoAlertDialogControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final Widget? nextChild;

  const CupertinoAlertDialogControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.nextChild});

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
    // final actionsAlignment = parseMainAxisAlignment(
    //     widget.control, "actionsAlignment", MainAxisAlignment.start);
    if (titleCtrls.isEmpty && contentCtrls.isEmpty && actionCtrls.isEmpty) {
      return const ErrorControl("AlertDialog does not have any content.");
    }

    return CupertinoAlertDialog(
      title: titleCtrls.isNotEmpty
          ? createControl(widget.control, titleCtrls.first.id, disabled)
          : null,
      //titlePadding: parseEdgeInsets(widget.control, "titlePadding"),
      content: contentCtrls.isNotEmpty
          ? createControl(widget.control, contentCtrls.first.id, disabled)
          : null,
      // contentPadding: parseEdgeInsets(widget.control, "contentPadding") ??
      //     const EdgeInsets.fromLTRB(24.0, 20.0, 24.0, 24.0),
      actions: actionCtrls
          .map((c) => createControl(widget.control, c.id, disabled))
          .toList(),
      //actionsPadding: parseEdgeInsets(widget.control, "actionsPadding"),
      //actionsAlignment: actionsAlignment,
      //shape: parseOutlinedBorder(widget.control, "shape"),
      // insetPadding: parseEdgeInsets(widget.control, "insetPadding") ??
      //     const EdgeInsets.symmetric(horizontal: 40.0, vertical: 24.0),
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoAlertDialog build ($hashCode): ${widget.control.id}");

    var server = FletAppServices.of(context).server;

    bool lastOpen = widget.control.state["open"] ?? false;

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint(
              "CupertinoAlertDialog StoreConnector build: ${widget.control.id}");

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
                  useRootNavigator: false,
                  context: context,
                  builder: (context) => dialog).then((value) {
                lastOpen = widget.control.state["open"] ?? false;
                debugPrint("Dialog should be dismissed ($hashCode): $lastOpen");
                bool shouldDismiss = lastOpen;
                widget.control.state["open"] = false;

                if (shouldDismiss) {
                  List<Map<String, String>> props = [
                    {"i": widget.control.id, "open": "false"}
                  ];
                  dispatch(UpdateControlPropsAction(
                      UpdateControlPropsPayload(props: props)));
                  server.updateControlProps(props: props);
                  server.sendPageEvent(
                      eventTarget: widget.control.id,
                      eventName: "dismiss",
                      eventData: "");
                }
              });
            });
          } else if (open != lastOpen && lastOpen) {
            Navigator.of(context).pop();
          }

          return widget.nextChild ?? const SizedBox.shrink();
        });
  }
}
