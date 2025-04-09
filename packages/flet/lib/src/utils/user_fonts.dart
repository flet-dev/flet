import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;

import '../models/control.dart';
import 'user_fonts_web.dart' if (dart.library.io) "user_fonts_io.dart";

class UserFonts {
  static Map<String, FontLoader> fontLoaders = {};

  static Future<void> loadFontFromUrl(String fontFamily, String fontUrl) async {
    var key = "$fontFamily$fontUrl";
    if (fontLoaders.containsKey(key)) return;
    debugPrint("Load font from URL: $fontUrl");
    var fontLoader = FontLoader(fontFamily);
    fontLoaders[key] = fontLoader;
    fontLoader.addFont(fetchFontFromUrl(fontUrl));
    await fontLoader.load();
    debugPrint("Font loaded from URL: $fontUrl");
  }

  static Future<void> loadFontFromFile(
      String fontFamily, String fontPath) async {
    var key = "$fontFamily$fontPath";
    if (fontLoaders.containsKey(key)) return;
    debugPrint("Load font from file: $fontPath");
    var fontLoader = FontLoader(fontFamily);
    fontLoaders[key] = fontLoader;
    fontLoader.addFont(fetchFontFromFile(fontPath));
    await fontLoader.load();
    debugPrint("Font loaded from file: $fontPath");
  }

  static Future<ByteData> fetchFontFromUrl(String url) async {
    final response = await http.get(Uri.parse(url));

    if (response.statusCode == 200) {
      return ByteData.view(response.bodyBytes.buffer);
    } else {
      // If that call was not successful, throw an error.
      throw Exception('Failed to load font $url');
    }
  }
}

Map<String, String>? parseFonts(dynamic value,
    [Map<String, String>? defaultValue]) {
  if (value == null) return {};
  return value.map((key, value) => MapEntry(key, value));
}

extension UserFontParsers on Control {
  Map<String, String>? getFonts(String propertyName,
      [Map<String, String>? defaultValue]) {
    return parseFonts(get(propertyName), defaultValue);
  }
}
