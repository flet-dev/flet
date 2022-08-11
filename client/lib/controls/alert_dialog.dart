import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/alignment.dart';
import '../utils/edge_insets.dart';
import '../web_socket_client.dart';
import 'create_control.dart';
import 'error.dart';

class AlertDialogControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const AlertDialogControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<AlertDialogControl> createState() => _AlertDialogControlState();
}

class _AlertDialogControlState extends State<AlertDialogControl> {
  bool _open = false;

  Widget _createAlertDialog() {
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var titleCtrls =
        widget.children.where((c) => c.name == "title" && c.isVisible);
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    var actionCtrls =
        widget.children.where((c) => c.name == "action" && c.isVisible);
    final actionsAlignment = parseMainAxisAlignment(
        widget.control, "actionsAlignment", MainAxisAlignment.start);
    if (titleCtrls.isEmpty && contentCtrls.isEmpty && actionCtrls.isEmpty) {
      return const ErrorControl("AlertDialog does not have any content.");
    }

    return AlertDialog(
      title: titleCtrls.isNotEmpty
          ? createControl(widget.control, titleCtrls.first.id, disabled)
          : null,
      titlePadding: parseEdgeInsets(widget.control, "titlePadding"),
      content: contentCtrls.isNotEmpty
          ? createControl(widget.control, contentCtrls.first.id, disabled)
          : null,
      contentPadding: parseEdgeInsets(widget.control, "contentPadding") ??
          const EdgeInsets.fromLTRB(24.0, 20.0, 24.0, 24.0),
      actions: actionCtrls
          .map((c) => createControl(widget.control, c.id, disabled))
          .toList(),
      actionsPadding: parseEdgeInsets(widget.control, "actionsPadding"),
      actionsAlignment: actionsAlignment,
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("AlertDialog build: ${widget.control.id}");

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint("AlertDialog StoreConnector build: ${widget.control.id}");

          var open = widget.control.attrBool("open", false)!;
          var modal = widget.control.attrBool("modal", false)!;
          // var removeCurrentSnackbar =
          //     widget.control.attrBool("removeCurrentSnackBar", false)!;

          debugPrint("Current open state: $_open");
          debugPrint("New open state: $open");

          if (open && (open != _open)) {
            var dialog = _createAlertDialog();
            if (dialog is ErrorControl) {
              return dialog;
            }

            WidgetsBinding.instance.addPostFrameCallback((_) {
              // if (removeCurrentSnackbar) {
              //   ScaffoldMessenger.of(context).removeCurrentSnackBar();
              // }

              showDialog(
                  barrierDismissible: !modal,
                  context: context,
                  builder: (context) => _createAlertDialog()).then((value) {
                debugPrint("Dialog dismissed: $_open");
                bool shouldDismiss = _open;
                _open = false;

                if (shouldDismiss) {
                  List<Map<String, String>> props = [
                    {"i": widget.control.id, "open": "false"}
                  ];
                  dispatch(UpdateControlPropsAction(
                      UpdateControlPropsPayload(props: props)));
                  ws.updateControlProps(props: props);
                  ws.pageEventFromWeb(
                      eventTarget: widget.control.id,
                      eventName: "dismiss",
                      eventData: "");
                }
              });
            });
          } else if (open != _open && _open) {
            Navigator.pop(context);
          }

          _open = open;

          return const SizedBox.shrink();
        });
  }
}
