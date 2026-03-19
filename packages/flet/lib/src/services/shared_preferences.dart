import 'package:flutter/cupertino.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../flet_service.dart';

class SharedPreferencesService extends FletService {
  SharedPreferencesService({required super.control});

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
    var prefs = await SharedPreferences.getInstance();
    switch (name) {
      case "set":
        var key = args["key"]!;
        var value = args["value"]!;

        if (value is String) return prefs.setString(key, value);
        if (value is bool) return prefs.setBool(key, value);
        if (value is int) return prefs.setInt(key, value);
        if (value is double) return prefs.setDouble(key, value);
        if (value is List && value.every((item) => item is String)) {
          return prefs.setStringList(key, value.cast<String>());
        }
        throw UnsupportedError(
            "Unsupported SharedPreferences value type: ${value.runtimeType}. "
            "Supported: String, bool, int, double, List<String>.");
      case "get":
        return prefs.get(args["key"]!);
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
