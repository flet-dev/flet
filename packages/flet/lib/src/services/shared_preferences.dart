import 'dart:convert';

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/widgets.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../flet_backend.dart';
import '../flet_service.dart';
import 'storage_lock_stub.dart'
    if (dart.library.js_interop) 'storage_lock_web.dart';

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
        prefs, control.backend.storagePrefix, name, args,
        quota: control.backend.sharedPreferencesQuota,
        ancestorQuotas: control.backend.ancestorPreferenceQuotas);
  }

  @override
  void dispose() {
    debugPrint("SharedPreferencesService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}

/// Runs one `ft.SharedPreferences` method against [prefs], with every key
/// under [prefix]. With an empty [prefix] this is the plain store. A `set`
/// that would take the app's keys and values past [quota] bytes fails.
@visibleForTesting
Future<dynamic> invokeSharedPreferencesMethod(
    SharedPreferences prefs, String prefix, String name, dynamic args,
    {int? quota, Map<String, int> ancestorQuotas = const {}}) async {
  String key() => prefix + args["key"]!;
  switch (name) {
    case "set":
      var value = args["value"]!;
      if (quota == null && ancestorQuotas.isEmpty) {
        return _set(prefs, key(), value);
      }
      // A single lock also covers overlapping ancestor and child prefixes.
      return withStorageLock("flet.shared_preferences.quota", () async {
        if (kIsWeb) await prefs.reload();
        for (final ancestor in ancestorQuotas.entries) {
          if (ancestor.key != prefix) {
            _checkQuota(prefs, ancestor.key, key(), value, ancestor.value);
          }
        }
        if (quota != null) _checkQuota(prefs, prefix, key(), value, quota);
        return _set(prefs, key(), value);
      });
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
      for (var k
          in prefs.getKeys().where((k) => k.startsWith(prefix)).toList()) {
        await prefs.remove(k);
      }
      return true;
    default:
      throw Exception("Unknown SharedPreferences method: $name");
  }
}

Future<bool> _set(SharedPreferences prefs, String key, Object value) {
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
}

/// Roughly what a key and its value take in the store, in bytes.
int _entrySize(String key, Object? value) =>
    utf8.encode(key).length + utf8.encode(jsonEncode(value)).length;

/// Throws if storing [value] under [key] would take the keys under [prefix]
/// past [quota] bytes. The key's current value doesn't count: it's replaced.
void _checkQuota(SharedPreferences prefs, String prefix, String key,
    Object value, int quota) {
  var used = 0;
  for (var k in prefs.getKeys()) {
    if (k.startsWith(prefix) && k != key) used += _entrySize(k, prefs.get(k));
  }
  var after = used + _entrySize(key, value);
  if (after > quota) {
    throw StateError(
        "Storing \"${key.substring(prefix.length)}\" would take this app's "
        "SharedPreferences to $after bytes, over its $quota-byte quota.");
  }
}
