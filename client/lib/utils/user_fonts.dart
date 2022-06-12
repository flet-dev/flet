import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;

import '../models/control.dart';

class UserFonts {
  static Map<String, FontLoader> fontLoaders = {};

  static void loadFont(String fontFamily, Uri fontUri) {
    var key = "$fontFamily$fontUri";
    if (fontLoaders.containsKey(key)) {
      return;
    }
    var fontLoader = FontLoader(fontFamily);
    fontLoaders[key] = fontLoader;
    fontLoader.addFont(fetchFont(fontUri));
    fontLoader.load();
  }

  static Future<ByteData> fetchFont(Uri uri) async {
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      return ByteData.view(response.bodyBytes.buffer);
    } else {
      // If that call was not successful, throw an error.
      throw Exception('Failed to load font $uri');
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
