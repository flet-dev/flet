import 'dart:convert';

import 'package:flet/src/utils/theme.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test("Light theme is parsed correctly from JSON", () {
    const t1 = '''{
        "color_scheme_seed": "red",
        "brightness": "light1",
        "use_material3": true
      }''';

    final j1 = json.decode(t1);
    var theme = themeFromJson(j1);

    expect(theme.brightness, Brightness.light);
    expect(theme.useMaterial3, true);
    expect(theme.primaryColor, const Color(0xffbb1614));
  });

  test("Dark theme is parsed correctly from JSON", () {
    const t1 = '''{
        "color_scheme_seed": "cyan",
        "brightness": "dark"
      }''';

    final j1 = json.decode(t1);
    var theme = themeFromJson(j1);

    expect(theme.brightness, Brightness.dark);
    expect(theme.useMaterial3, false);
    expect(theme.primaryColor, const Color(0xff191c1d));
  });
}
