import 'package:flutter/material.dart';

import '../models/control.dart';
import '../web_socket_client.dart';

class ButtonControl extends StatelessWidget {
  final Control control;
  final bool disabled;

  const ButtonControl({Key? key, required this.control, required this.disabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Button build: ${control.id}");
    return SizedBox(
      child: ElevatedButton(
        onPressed: () {
          debugPrint("Button ${control.id} clicked!");
          ws.pageEventFromWeb(
              eventTarget: control.id,
              eventName: "click",
              eventData: control.attrs["data"] ?? "");
        },
        child: Text(control.attrs["text"] ?? ""),
      ),
    );
  }
}
