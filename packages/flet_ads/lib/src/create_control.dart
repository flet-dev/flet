import 'package:flet/flet.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

import 'banner.dart';
import 'interstitial.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "banner_ad":
      return BannerAdControl(
          parent: args.parent, control: args.control, backend: args.backend);
    case "interstitial_ad":
      return InterstitialAdControl(
          parent: args.parent, control: args.control, backend: args.backend);
    /* TODO: Finalize NativeAdControl -> https://developers.google.com/admob/flutter/native/platforms
    case "native_ad":
      return NativeAdControl(
          parent: args.parent, control: args.control, backend: args.backend);
    */
    default:
      return null;
  }
};

void ensureInitialized() {
  if (isMobilePlatform()) {
    MobileAds.instance.initialize();
  }
}
