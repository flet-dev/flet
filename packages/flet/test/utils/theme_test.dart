import 'dart:convert';

import 'package:flet/src/utils/theme.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test("Light theme is parsed correctly from JSON", () {
    const t1 = '''{
        "color_scheme_seed": "red",
        "brightness": "light",
        "use_material3": false
      }''';

    final j1 = json.decode(t1);
    var theme = themeFromJson(j1, Brightness.light, null);

    expect(theme.brightness, Brightness.light);
    expect(theme.useMaterial3, false);
    expect(theme.primaryColor, const Color(0xff904a42));
  });

  test("Dark theme is parsed correctly from JSON", () {
    const t1 = '''{
        "color_scheme_seed": "cyan",
        "brightness": "dark"
      }''';

    final j1 = json.decode(t1);
    var theme = themeFromJson(j1, Brightness.dark, null);

    expect(theme.brightness, Brightness.dark);
    expect(theme.useMaterial3, true);
    expect(theme.primaryColor, const Color(0xff0e1416));
  });
}
