import 'package:flutter/foundation.dart';
// ignore: avoid_web_libraries_in_flutter
import 'package:web/web.dart' as web;

const String _sessionIdKey = "_flet_session_id";

class SessionStore {
  static String? get sessionId {
    return get(_sessionIdKey);
  }

  static set sessionId(String? value) {
    set(_sessionIdKey, value ?? "");
  }

  static String? get(String name) {
    debugPrint("Get session storage $name");
    return web.window.sessionStorage.getItem(name);
  }

  static void set(String name, String value) {
    debugPrint("Set session storage $name");
    web.window.sessionStorage.setItem(name, value);
  }
}
