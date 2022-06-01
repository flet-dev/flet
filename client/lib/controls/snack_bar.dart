import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../web_socket_client.dart';
import 'create_control.dart';
import 'error.dart';

class SnackBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const SnackBarControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<SnackBarControl> createState() => _SnackBarControlState();
}

class _SnackBarControlState extends State<SnackBarControl> {
  bool _open = false;

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    super.dispose();
  }

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
            onPressed: () {
              debugPrint("SnackBar ${widget.control.id} clicked!");
              ws.pageEventFromWeb(
                  eventTarget: widget.control.id,
                  eventName: "action",
                  eventData: widget.control.attrs["data"] ?? "");
            })
        : null;

    return SnackBar(
        content: createControl(widget.control, contentCtrls.first.id, disabled),
        action: action);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SnackBar build: ${widget.control.id}");

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint("SnackBar StoreConnector build: ${widget.control.id}");

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

              List<Map<String, String>> props = [
                {"i": widget.control.id, "open": "false"}
              ];
              dispatch(UpdateControlPropsAction(
                  UpdateControlPropsPayload(props: props)));
              ws.updateControlProps(props: props);
            });
          }

          _open = open;

          return const SizedBox.shrink();
        });
  }
}
