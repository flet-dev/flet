import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';


class EchoTextControl extends StatefulWidget {
  final Control? parent;
  final Control control;

  const EchoTextControl(
    {Key? key,
   this.parent,
   required this.control}
  ) : super(key: key);

  @override
  State<EchoTextControl> createState() => _EchoTextControlState();
}

class _EchoTextControlState extends State<EchoTextControl> {
  String _message = "";
  String _echoed = "N/A";

  @override
  Widget build(BuildContext context) {
    final ws = FletAppServices.of(context).ws;  // websocket

    Function() onPress = () {
      ws.pageEventFromWeb(
        eventTarget: widget.control.id,
        eventName: "click",
        eventData: "",
      );
    };

    return StoreConnector<AppState, Function>(
      distinct: true,
      converter: (store) => store.dispatch,
      builder: (context, dispatch) {
        String message = widget.control.attrs["message"] ?? "";
        if (_message != message) {
          _message = message;
        }
        String echoed = widget.control.attrs["echoed"] ?? "";
        if (_echoed != echoed) {
          _echoed = echoed;
        }

        return Column(
          children: [
            TextFormField(
              onChanged: (String value) {
                setState(() {
                    _message = value;
                });
                List<Map<String, String>> props = [
                  {"i": widget.control.id, "message": value}
                ];
                ws.updateControlProps(props: props);
                ws.pageEventFromWeb(
                  eventTarget: widget.control.id,
                  eventName: "change",
                  eventData: value,
                );
              },
              initialValue: _message,
            ),
            TextButton(
              onPressed: onPress,
              child: const Text("send")
            ),
            Text(echoed)
          ]
        );
      });
  }
}
