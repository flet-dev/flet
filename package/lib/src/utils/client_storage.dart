import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../flet_server.dart';
import '../protocol/invoke_method_result.dart';

void invokeClientStorage(String methodId, String methodName,
    Map<String, String> args, FletServer server) async {
  sendResult(Object? result, String? error) {
    server.sendPageEvent(
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
              .where((key) => key.startsWith(args["key_prefix"]!))
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
