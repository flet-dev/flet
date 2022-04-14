import 'package:flet_view/controls/create_control.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../web_socket_client.dart';

class ElevatedButtonControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const ElevatedButtonControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Button build: ${control.id}");

    bool disabled = control.isDisabled || parentDisabled;

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

    return expandable(button, parent, control);
  }
}
