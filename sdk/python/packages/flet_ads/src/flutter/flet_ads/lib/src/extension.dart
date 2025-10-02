import 'package:flet/flet.dart';
import 'package:flutter/cupertino.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

import 'banner.dart';
import 'interstitial.dart';

class Extension extends FletExtension {
  @override
  void ensureInitialized() {
    if (isMobilePlatform()) {
      MobileAds.instance.initialize();
    }
  }

  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "InterstitialAd":
        return InterstitialAdService(control: control);
      default:
        return null;
    }
  }

  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "BannerAd":
        return BannerAdControl(control: control);
      /* TODO: Finalize NativeAdControl -> https://developers.google.com/admob/flutter/native/platforms
      case "NativeAd":
        return NativeAdControl(control: control);
      */
      default:
        return null;
    }
  }
}
