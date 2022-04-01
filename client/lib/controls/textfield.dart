import 'package:flutter/material.dart';
import 'package:flet_view/protocol/update_control_props_payload.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../web_socket_client.dart';

class TextFieldControl extends StatefulWidget {
  final Control control;

  const TextFieldControl({Key? key, required this.control}) : super(key: key);

  @override
  State<TextFieldControl> createState() => _TextFieldControlState();
}

class _TextFieldControlState extends State<TextFieldControl> {
  String _value = "";
  late TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("TextField build: ${widget.control.id}");
    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint("TextField StoreConnector build: ${widget.control.id}");

          String value = widget.control.attrs["value"] ?? "";
          if (_value != value) {
            _value = value;
            _controller.text = value;
          }

          return TextFormField(
              //initialValue: widget.control.attrs["value"] ?? "",
              decoration: InputDecoration(
                  labelText: widget.control.attrs["label"] ?? "",
                  border: const OutlineInputBorder()),
              controller: _controller,
              onChanged: (String value) {
                debugPrint(value);
                setState(() {
                  _value = value;
                });
                List<Map<String, String>> props = [
                  {"i": widget.control.id, "value": value}
                ];
                dispatch(UpdateControlPropsAction(
                    UpdateControlPropsPayload(props: props)));
                ws.updateControlProps(props: props);
              });
        });
  }
}
