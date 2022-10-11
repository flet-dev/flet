import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';

class ClipboardControl extends StatefulWidget {
  final Control? parent;
  final Control control;

  const ClipboardControl(
      {Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  State<ClipboardControl> createState() => _ClipboardControlState();
}

class _ClipboardControlState extends State<ClipboardControl> {
  String? _method;

  @override
  Widget build(BuildContext context) {
    debugPrint("Clipboard build: ${widget.control.id}");

    () async {
      var method = widget.control.attrString("method");
      if (method != null && method != _method) {
        _method = method;
        debugPrint("Clipboard JSON value: $_method");

        List<Map<String, String>> props = [
          {"i": widget.control.id, "method": ""}
        ];
        FletAppServices.of(context).store.dispatch(
            UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
        FletAppServices.of(context).ws.updateControlProps(props: props);

        var mj = json.decode(method);
        var i = mj["i"] as int;
        var name = mj["n"] as String;
        var params = List<String>.from(mj["p"] as List);

        sendResult(Object? result, String? error) {
          FletAppServices.of(context).ws.pageEventFromWeb(
              eventTarget: widget.control.id,
              eventName: "method_result",
              eventData: json.encode({
                "i": i,
                "r": result != null ? json.encode(result) : null,
                "e": error
              }));
        }

        switch (name) {
          case "set_data":
            Clipboard.setData(ClipboardData(text: params[0]));
            break;
          case "get_data":
            String? r;
            String? ex;
            try {
              r = (await Clipboard.getData(Clipboard.kTextPlain))?.text;
            } catch (e) {
              ex = e.toString();
            }
            sendResult(r, ex);
            break;
        }
      }
    }();

    return const SizedBox.shrink();
  }
}
