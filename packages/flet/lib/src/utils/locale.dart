import 'package:flutter/material.dart';

import '../models/control.dart';

class LocaleConfiguration {
  final List<Locale> supportedLocales;
  final Locale? locale;

  const LocaleConfiguration(
      {required this.supportedLocales, required this.locale});
}

LocaleConfiguration parseLocaleConfiguration(dynamic value) {
  List<Locale>? supportedLocales;
  Locale? locale;

  if (value != null) {
    var sl = value["supported_locales"];
    if (sl != null) {
      supportedLocales =
          sl.map((e) => parseLocale(e)).whereType<Locale>().toList();
    }
    locale = parseLocale(value["current_locale"]);
  }

  return LocaleConfiguration(
      supportedLocales: supportedLocales != null && supportedLocales.isNotEmpty
          ? supportedLocales
          : [const Locale("en", "US")],
      locale: locale);
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

extension LocaleParsers on Control {
  LocaleConfiguration getLocaleConfiguration(String propertyName,
      [LocaleConfiguration? defaultValue]) {
    return parseLocaleConfiguration(get(propertyName));
  }

  Locale? getLocale(String propertyName, [Locale? defaultValue]) {
    return parseLocale(get(propertyName), defaultValue);
  }
}
