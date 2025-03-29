import 'package:flutter/cupertino.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../flet_service.dart';

class SharedPreferencesService extends FletService {
  SharedPreferencesService(super.control, super.backend);

  @override
  void init() {
    super.init();
    debugPrint(
        "SharedPreferencesService(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void update() {
    debugPrint(
        "SharedPreferencesService(${control.id}).update: ${control.properties}");
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("SharedPreferencesService.$name($args)");
    var prefs = await SharedPreferences.getInstance();
    switch (name) {
      case "set":
        return prefs.setString(args["key"]!, args["value"]!);
      case "get":
        return prefs.getString(args["key"]!);
      case "contains_key":
        return prefs.containsKey(args["key"]!);
      case "get_keys":
        return prefs
            .getKeys()
            .where((key) => key.startsWith(args["key_prefix"]!))
            .toList();
      case "remove":
        return prefs.remove(args["key"]!);
      case "clear":
        return prefs.clear();
      default:
        throw Exception("Unknown SharedPreferences method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("SharedPreferencesService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
