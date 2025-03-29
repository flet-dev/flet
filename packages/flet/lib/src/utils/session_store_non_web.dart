import 'package:flutter/foundation.dart';

class SessionStore {
  static String? sessionId;

  static String? get(String name) {
    if (name == "sessionId") return sessionId;
    return null;
  }

  static void set(String name, String value) {
    debugPrint("Do not set cookie!");
  }
}
