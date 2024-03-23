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
  Locale? locale = json["current_locale"] != null
      ? localeFromJSON(json["current_locale"])
      : null;
  if (sl != null) {
    supportedLocales =
        sl.map((e) => localeFromJSON(e)).whereType<Locale>().toList();
  }

  return {
    "supportedLocales": supportedLocales != null && supportedLocales.isNotEmpty
        ? supportedLocales
        : [const Locale("en", "US")], // American locale as fallback
    "locale": locale
  };
}

Locale localeFromJSON(dynamic json) {
  var languageCode = json["language_code"]?.trim();
  var countryCode = json["country_code"]?.trim();
  var scriptCode = json["script_code"]?.trim();
  return Locale.fromSubtags(
      languageCode: (languageCode != null && languageCode.isNotEmpty)
          ? languageCode
          : "und", // und = undefined language code
      countryCode:
          (countryCode != null && countryCode.isNotEmpty) ? countryCode : null,
      scriptCode:
          (scriptCode != null && scriptCode.isNotEmpty) ? scriptCode : null);
}
