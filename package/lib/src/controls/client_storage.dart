import 'dart:convert';

import 'package:flet/src/flet_app_services.dart';
import 'package:flutter/widgets.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../models/control.dart';

class ClientStorageControl extends StatefulWidget {
  final Control? parent;
  final Control control;

  const ClientStorageControl(
      {Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  State<ClientStorageControl> createState() => _ClientStorageControlState();
}

class _ClientStorageControlState extends State<ClientStorageControl> {
  String? _method;

  @override
  Widget build(BuildContext context) {
    debugPrint("Client storage build: ${widget.control.id}");

    var method = widget.control.attrString("method");

    if (method != null && method != _method) {
      _method = method;
      debugPrint("Client storage JSON value: $_method");

      var mj = json.decode(method);
      var i = mj["i"] as int;
      var name = mj["n"] as String;
      var params = List<String>.from(mj["p"] as List);

      sendResult(Object? result, String? error) {
        FletAppServices.of(context).ws.pageEventFromWeb(
            eventTarget: widget.control.id,
            eventName: "result",
            eventData: json.encode({
              "i": i,
              "r": result != null ? json.encode(result) : null,
              "e": error
            }));
      }

      () async {
        var prefs = await SharedPreferences.getInstance();
        if (name == "set") {
          var result = await prefs.setString(params[0], params[1]);
          sendResult(result, null);
        } else if (name == "get") {
          sendResult(prefs.getString(params[0]), null);
        }
      }();
    }

    return const SizedBox.shrink();
  }
}
