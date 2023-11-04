import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/control_global_state.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';

class AlertDialogControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final Widget? nextChild;

  const AlertDialogControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.nextChild})
      : super(key: key);

  @override
  State<AlertDialogControl> createState() => _AlertDialogControlState();
}

class _AlertDialogControlState extends State<AlertDialogControl> {
  String? _id;
  ControlsGlobalState? _globalState;

  @override
  void initState() {
    super.initState();
    debugPrint("AlertDialog initState() ($hashCode)");
  }

  @override
  void dispose() {
    debugPrint("AlertDialog dispose() ($hashCode)");
    if (_id != null) {
      _globalState?.remove(_id!, "open", hashCode);
    }
    super.dispose();
  }

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
      shape: parseOutlinedBorder(widget.control, "shape"),
      insetPadding: parseEdgeInsets(widget.control, "insetPadding") ??
          const EdgeInsets.symmetric(horizontal: 40.0, vertical: 24.0),
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("AlertDialog build ($hashCode): ${widget.control.id}");

    _id = widget.control.id;
    _globalState = FletAppServices.of(context).globalState;
    var server = FletAppServices.of(context).server;

    bool lastOpen = _globalState?.get(widget.control.id, "open") ?? false;

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint("AlertDialog StoreConnector build: ${widget.control.id}");

          var open = widget.control.attrBool("open", false)!;
          var modal = widget.control.attrBool("modal", false)!;

          debugPrint("Current open state: $lastOpen");
          debugPrint("New open state: $open");

          if (open && (open != lastOpen)) {
            var dialog = _createAlertDialog();
            if (dialog is ErrorControl) {
              return dialog;
            }

            _globalState?.set(widget.control.id, "open", open, hashCode);

            WidgetsBinding.instance.addPostFrameCallback((_) {
              showDialog(
                  barrierDismissible: !modal,
                  context: context,
                  builder: (context) => _createAlertDialog()).then((value) {
                lastOpen =
                    _globalState?.get(widget.control.id, "open") ?? false;
                debugPrint("Dialog should be dismissed ($hashCode): $lastOpen");
                bool shouldDismiss = lastOpen;
                _globalState?.set(widget.control.id, "open", false, hashCode);

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
            Navigator.pop(context);
          }

          return widget.nextChild ?? const SizedBox.shrink();
        });
  }
}
