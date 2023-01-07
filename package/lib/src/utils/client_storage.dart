import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../protocol/invoke_method_result.dart';
import '../flet_server.dart';

void invokeClientStorage(String methodId, String methodName,
    Map<String, String> args, FletServer ws) async {
  sendResult(Object? result, String? error) {
    ws.pageEventFromWeb(
        eventTarget: "page",
        eventName: "invoke_method_result",
        eventData: json.encode(InvokeMethodResult(
            methodId: methodId,
            result: result != null ? json.encode(result) : null,
            error: error)));
  }

  var prefs = await SharedPreferences.getInstance();
  switch (methodName) {
    case "set":
      var result = await prefs.setString(args["key"]!, args["value"]!);
      sendResult(result, null);
      break;
    case "get":
      sendResult(prefs.getString(args["key"]!), null);
      break;
    case "containskey":
      sendResult(prefs.containsKey(args["key"]!), null);
      break;
    case "getkeys":
      sendResult(
          prefs
              .getKeys()
              .where((key) => key.startsWith(args["prefix"]!))
              .toList(),
          null);
      break;
    case "remove":
      sendResult(await prefs.remove(args["key"]!), null);
      break;
    case "clear":
      sendResult(await prefs.clear(), null);
      break;
  }
}
