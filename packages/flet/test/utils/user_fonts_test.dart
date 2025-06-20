import 'package:flet/src/utils/user_fonts.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test("Custom fonts are parsed from JSON", () {
    const t1 = {
      "font1": "https://fonts.com/font1.ttf",
      "font2": "https://fonts.com/font2.ttf"
    };

    var fonts = parseFonts(t1)!;

    expect(fonts.length, 2);
    expect(fonts["font1"], "https://fonts.com/font1.ttf");
    expect(fonts["font2"], "https://fonts.com/font2.ttf");
  });
}
