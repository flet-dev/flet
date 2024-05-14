import 'package:flet/flet.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

import 'banner.dart';
import 'interstitial.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "bannerad":
      return BannerAdControl(
          parent: args.parent, control: args.control, backend: args.backend);
    case "interstitialad":
      return InterstitialAdControl(
          parent: args.parent, control: args.control, backend: args.backend);
    default:
      return null;
  }
};

void ensureInitialized() {
  MobileAds.instance.initialize();
}
