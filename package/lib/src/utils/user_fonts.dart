import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;

import '../models/control.dart';

import 'user_fonts_io.dart' if (dart.library.js) "user_fonts_web.dart";

class UserFonts {
  static Map<String, FontLoader> fontLoaders = {};

  static void loadFontFromUrl(String fontFamily, String fontUrl) {
    debugPrint("Load font from URL: $fontUrl");
    var key = "$fontFamily$fontUrl";
    if (fontLoaders.containsKey(key)) {
      return;
    }
    var fontLoader = FontLoader(fontFamily);
    fontLoaders[key] = fontLoader;
    fontLoader.addFont(fetchFontFromUrl(fontUrl));
    fontLoader.load();
  }

  static void loadFontFromFile(String fontFamily, String fontPath) {
    debugPrint("Load font from file: $fontPath");
    var key = "$fontFamily$fontPath";
    if (fontLoaders.containsKey(key)) {
      return;
    }
    var fontLoader = FontLoader(fontFamily);
    fontLoaders[key] = fontLoader;
    fontLoader.addFont(fetchFontFromFile(fontPath));
    fontLoader.load();
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

Map<String, String> parseFonts(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return {};
  }

  final j1 = json.decode(v);
  return fontsFromJson(j1);
}

Map<String, String> fontsFromJson(Map<String, dynamic> json) {
  return json.map((key, value) => MapEntry(key, value));
}
