import 'package:flet_view/controls/create_control.dart';
import 'package:flutter/material.dart';
import 'package:flet_view/protocol/update_control_props_payload.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../web_socket_client.dart';

class SnackBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const SnackBarControl(
      {Key? key,
      this.parent,
      required this.control,
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

  @override
  Widget build(BuildContext context) {
    debugPrint("SnackBar build: ${widget.control.id}");

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint("SnackBar StoreConnector build: ${widget.control.id}");

          // bool disabled = widget.control.attrBool("disabled", false)! ||
          //     widget.parentDisabled;

          var open = widget.control.attrBool("open", false)!;

          debugPrint("Current open state: $_open");
          debugPrint("New open state: $open");

          if (open && (open != _open)) {
            WidgetsBinding.instance!.addPostFrameCallback((_) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                content: Text(widget.control.attrString("content", "")!),
              ));

              List<Map<String, String>> props = [
                {"i": widget.control.id, "open": "false"}
              ];
              dispatch(UpdateControlPropsAction(
                  UpdateControlPropsPayload(props: props)));
              ws.updateControlProps(props: props);
            });
          }

          _open = open;

          // if (open != _open) {
          //   setState(() {
          //     _open = open;
          //   });
          // }
          // String value = widget.control.attrs["value"] ?? "";
          // if (_value != value) {
          //   _value = value;
          //   _controller.text = value;
          // }

          // _snackBar = SnackBar(
          //   content: Text(widget.control.attrString("content", "")!),
          // );

          // bool open = widget.control.attrBool("open", false)!;
          // if (open) {
          //   ScaffoldMessenger.of(context).showSnackBar(snackBar);
          // }

          return const SizedBox.shrink();
        });
  }
}
