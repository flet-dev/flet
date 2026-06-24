import 'package:flet/flet.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

DebugGeography? parseDebugGeography(String? value,
        [DebugGeography? defaultValue]) =>
    parseEnum(DebugGeography.values, "debugGeography$value", defaultValue);

ConsentDebugSettings? parseConsentDebugSettings(dynamic value,
    [ConsentDebugSettings? defaultValue]) {
  if (value == null) return defaultValue;
  return ConsentDebugSettings(
    debugGeography: parseDebugGeography(value["debug_geography"]),
    testIdentifiers:
        (value["test_identifiers"] as List?)?.map((e) => e.toString()).toList(),
  );
}

ConsentRequestParameters parseConsentRequestParameters(dynamic value) {
  if (value == null) return ConsentRequestParameters();
  return ConsentRequestParameters(
    tagForUnderAgeOfConsent: value["tag_for_under_age_of_consent"],
    consentDebugSettings:
        parseConsentDebugSettings(value["consent_debug_settings"]),
  );
}
