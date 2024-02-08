// ignore: avoid_web_libraries_in_flutter
import 'dart:html' as html;

import 'package:flutter/foundation.dart';

class SessionStore {
  static String? get sessionId {
    return html.window.name;
  }

  static set sessionId(String? value) {
    html.window.name = value;
  }

  static String? get(String name) {
    debugPrint("Get session storage $name");

    return html.window.sessionStorage[name];
  }

  static void set(String name, String value) {
    debugPrint("Set session storage $name");
    html.window.sessionStorage[name] = value;
  }
}
