import 'package:flutter/foundation.dart';

class SessionStore {
  static String? sessionId;

  static String? getSessionId(String pageUrl) {
    return get("sessionId");
  }

  static setSessionId(String pageUrl, String? value) {
    set("sessionId", value ?? "");
  }

  static String? get(String name) {
    return null;
  }

  static void set(String name, String value) {
    debugPrint("Do not set cookie!");
  }
}
