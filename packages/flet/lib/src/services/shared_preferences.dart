import 'package:flutter/widgets.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../flet_backend.dart';
import '../flet_service.dart';

/// `ft.SharedPreferences`. Every key is stored under the app's
/// [FletBackend.storagePrefix], so each app has its own space in the store:
/// an embedded app and its host, or two embedded apps, keep separate keys.
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
    return invokeSharedPreferencesMethod(
        prefs, control.backend.storagePrefix, name, args);
  }

  @override
  void dispose() {
    debugPrint("SharedPreferencesService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}

/// Runs one `ft.SharedPreferences` method against [prefs], with every key
/// under [prefix]. With an empty [prefix] this is the plain store.
@visibleForTesting
Future<dynamic> invokeSharedPreferencesMethod(
    SharedPreferences prefs, String prefix, String name, dynamic args) async {
  String key() => prefix + args["key"]!;
  switch (name) {
    case "set":
      var value = args["value"]!;
      if (value is String) return prefs.setString(key(), value);
      if (value is bool) return prefs.setBool(key(), value);
      if (value is int) return prefs.setInt(key(), value);
      if (value is double) return prefs.setDouble(key(), value);
      if (value is List && value.every((item) => item is String)) {
        return prefs.setStringList(key(), value.cast<String>());
      }
      throw UnsupportedError(
          "Unsupported SharedPreferences value type: ${value.runtimeType}. "
          "Supported: String, bool, int, double, List<String>.");
    case "get":
      return prefs.get(key());
    case "contains_key":
      return prefs.containsKey(key());
    case "get_keys":
      // Listed without the prefix: the app sees the names it stored.
      var start = prefix + args["key_prefix"]!;
      return prefs
          .getKeys()
          .where((k) => k.startsWith(start))
          .map((k) => k.substring(prefix.length))
          .toList();
    case "remove":
      return prefs.remove(key());
    case "clear":
      if (prefix.isEmpty) return prefs.clear();
      // Only this app's keys - never its host's or another app's.
      for (var k in prefs.getKeys().where((k) => k.startsWith(prefix)).toList()) {
        await prefs.remove(k);
      }
      return true;
    default:
      throw Exception("Unknown SharedPreferences method: $name");
  }
}
