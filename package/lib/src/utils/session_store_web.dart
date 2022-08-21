import 'dart:html';

import 'package:flutter/foundation.dart';

class SessionStore {
  static String? get(String name) {
    debugPrint("Get session storage $name");

    return window.sessionStorage[name];
  }

  static void set(String name, String value) {
    debugPrint("Set session storage $name");
    window.sessionStorage[name] = value;
  }
}
