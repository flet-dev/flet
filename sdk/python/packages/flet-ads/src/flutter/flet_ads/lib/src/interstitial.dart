import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

import '../utils/ads.dart';

class InterstitialAdService extends FletService {
  InterstitialAdService({required super.control});

  static InterstitialAd? _interstitialAd;

  @override
  void init() {
    super.init();
    debugPrint("InterstitialAd(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);

    InterstitialAd.load(
        adUnitId: control.getString(
            "unit_id",
            isIOSMobile()
                ? 'ca-app-pub-3940256099942544/4411468910'
                : 'ca-app-pub-3940256099942544/1033173712')!,
        request: parseAdRequest(control.get("request"), const AdRequest())!,
        adLoadCallback: InterstitialAdLoadCallback(
          onAdLoaded: (ad) {
            ad.fullScreenContentCallback = FullScreenContentCallback(
              onAdShowedFullScreenContent: (ad) => control.triggerEvent("open"),
              onAdImpression: (ad) => control.triggerEvent("impression"),
              onAdFailedToShowFullScreenContent: (ad, error) {
                control.triggerEvent("error", error.toString());
                ad.dispose(); // free resources
              },
              onAdDismissedFullScreenContent: (ad) {
                // Called when the ad dismissed full screen content.
                control.triggerEvent("close");
                // Dispose the ad here to free resources.
                ad.dispose();
              },
              onAdClicked: (ad) => control.triggerEvent("click"),
            );

            // Keep a reference to show it later.
            _interstitialAd = ad;
            control.triggerEvent("load");
          },
          onAdFailedToLoad: (LoadAdError error) {
            control.triggerEvent("error", error.toString());
            _interstitialAd?.dispose();
          },
        ));
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("InterstitialAd.$name($args)");
    switch (name) {
      case "show":
        _interstitialAd?.show();
        return null;
      default:
        throw Exception("Unknown InterstitialAd method: $name");
    }
  }

  @override
  void dispose() {
    _interstitialAd?.dispose();
    super.dispose();
  }
}
