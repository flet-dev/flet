import 'package:flet_view/controls/create_control.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../web_socket_client.dart';

class ButtonControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const ButtonControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Button build: ${control.id}");

    bool disabled = control.attrBool("disabled", false) || parentDisabled;

    var button = ElevatedButton(
      onPressed: disabled
          ? null
          : () {
              debugPrint("Button ${control.id} clicked!");
              ws.pageEventFromWeb(
                  eventTarget: control.id,
                  eventName: "click",
                  eventData: control.attrs["data"] ?? "");
            },
      child: Text(control.attrs["text"] ?? ""),
    );

    return SizedBox(
      child: expandable(button, control),
    );
  }
}
