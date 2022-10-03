import 'package:flutter/foundation.dart';
import 'package:universal_html/html.dart';

class SessionStore {
  static String? get(String name) {
    debugPrint("Get session storage $name");

    return kIsWeb ? window.sessionStorage[name] : null;
  }

  static void set(String name, String value) {
    debugPrint("Set session storage $name");
    if (kIsWeb) {
      window.sessionStorage[name] = value;
    }
  }
}
