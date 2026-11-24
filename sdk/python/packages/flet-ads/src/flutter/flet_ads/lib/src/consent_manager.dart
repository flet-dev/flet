import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

import '../utils/consent.dart';

class ConsentManagerService extends FletService {
  ConsentManagerService({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("ConsentManager(${control.id}).init");
    control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("ConsentManager.$name($args)");
    switch (name) {
      case "request_consent_info_update":
        final completer = Completer<void>();
        ConsentInformation.instance.requestConsentInfoUpdate(
          parseConsentRequestParameters(args?["params"]),
          () {
            if (!completer.isCompleted) completer.complete();
          },
          (FormError error) {
            if (!completer.isCompleted) {
              completer.completeError(Exception(
                  "Consent info update failed (${error.errorCode}): ${error.message}"));
            }
          },
        );
        return completer.future;

      case "is_consent_form_available":
        return await ConsentInformation.instance.isConsentFormAvailable();

      case "get_consent_status":
        return (await ConsentInformation.instance.getConsentStatus()).name;

      case "can_request_ads":
        return await ConsentInformation.instance.canRequestAds();

      case "get_privacy_options_requirement_status":
        return (await ConsentInformation.instance
                .getPrivacyOptionsRequirementStatus())
            .name;

      case "load_and_show_consent_form_if_required":
        final completer = Completer<void>();
        ConsentForm.loadAndShowConsentFormIfRequired((FormError? error) {
          if (completer.isCompleted) return;
          if (error != null) {
            completer.completeError(Exception(
                "Consent form error (${error.errorCode}): ${error.message}"));
          } else {
            completer.complete();
          }
        });
        return completer.future;

      case "show_privacy_options_form":
        final completer = Completer<void>();
        ConsentForm.showPrivacyOptionsForm((FormError? error) {
          if (completer.isCompleted) return;
          if (error != null) {
            completer.completeError(Exception(
                "Privacy options form error (${error.errorCode}): ${error.message}"));
          } else {
            completer.complete();
          }
        });
        return completer.future;

      case "reset":
        return await ConsentInformation.instance.reset();

      default:
        throw Exception("Unknown ConsentManager method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("ConsentManager(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
