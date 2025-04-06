import 'package:flutter/material.dart';

Map<String, dynamic>? parseLocaleConfiguration(dynamic value,
    [Map<String, dynamic>? defaultValue]) {
  if (value == null) return defaultValue;
  List<Locale>? supportedLocales;

  var sl = value["supported_locales"];
  Locale? locale = parseLocale(value["current_locale"]);
  if (sl != null) {
    supportedLocales =
        sl.map((e) => parseLocale(e)).whereType<Locale>().toList();
  }

  return {
    "supportedLocales": supportedLocales != null && supportedLocales.isNotEmpty
        ? supportedLocales
        : [const Locale("en", "US")], // American locale as fallback
    "locale": locale
  };
}

Locale? parseLocale(dynamic value, [Locale? defaultValue]) {
  if (value == null) return defaultValue;
  var languageCode = value["language_code"]?.trim();
  var countryCode = value["country_code"]?.trim();
  var scriptCode = value["script_code"]?.trim();
  return Locale.fromSubtags(
      languageCode: (languageCode != null && languageCode.isNotEmpty)
          ? languageCode
          : "und", // und = undefined language code
      countryCode:
          (countryCode != null && countryCode.isNotEmpty) ? countryCode : null,
      scriptCode:
          (scriptCode != null && scriptCode.isNotEmpty) ? scriptCode : null);
}
