import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';

Map<String, dynamic>? parseLocaleConfiguration(
    Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return localeConfigurationFromJSON(j1);
}

Map<String, dynamic> localeConfigurationFromJSON(dynamic json) {
  List<Locale>? supportedLocales;
  var sl = json["supported_locales"];
  var locale =
      json["used_locale"] != null ? parseLocale(json["used_locale"]) : null;
  if (sl != null) {
    supportedLocales =
        sl.map((e) => parseLocale(e)).whereType<Locale>().toList();
  }

  return {
    "supportedLocales": supportedLocales != null && supportedLocales.isNotEmpty
        ? supportedLocales
        : [const Locale("en", "US")],
    "locale": locale
  };
}

Locale? parseLocale(value) {
  var languageCode = value["language_code"];
  if (languageCode != null && languageCode.trim().isNotEmpty) {
    var countryCode = value["country_code"];
    return Locale(languageCode, countryCode);
  }
  return null;
}

Locale? localeFromJSON(dynamic json) {
  String? languageCode = json["language_code"];
  if (languageCode != null && languageCode.trim().isNotEmpty) {
    String? countryCode = json["country_code"];
    return Locale(languageCode, countryCode);
  }
  return null;
}
