import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

class BannerAdControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const BannerAdControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.backend});

  @override
  State<BannerAdControl> createState() => _BannerAdControlState();
}

class _BannerAdControlState extends State<BannerAdControl> with FletStoreMixin {
  bool _isLoaded = false;

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "BannerAd build: ${widget.control.id} (${widget.control.hashCode})");
    return withPagePlatform((context, platform) {
      final testAdUnitId = platform == TargetPlatform.iOS
          ? 'ca-app-pub-3940256099942544/4411468910'
          : 'ca-app-pub-3940256099942544/1033173712';
      BannerAd bannerAd = BannerAd(
        adUnitId: widget.control.attrString("unitId", testAdUnitId)!,
        request: const AdRequest(),
        size: AdSize.banner,
        listener: BannerAdListener(
          // Called when an ad is successfully received.
          onAdLoaded: (ad) {
            widget.backend.triggerControlEvent(widget.control.id, "load");
            setState(() {
              _isLoaded = true;
            });
          },
          // Called when an ad request failed.
          onAdFailedToLoad: (ad, error) {
            widget.backend.triggerControlEvent(
                widget.control.id, "error", error.toString());
            debugPrint("BANNER AD failed to load: $error");
            // Dispose the ad to free resources.
            ad.dispose();
            setState(() {
              _isLoaded = false;
            });
          },
          // Called when an ad opens an overlay that covers the screen.
          onAdOpened: (Ad ad) {
            widget.backend.triggerControlEvent(widget.control.id, "open");
          },
          // Called when an ad removes an overlay that covers the screen.
          onAdClosed: (Ad ad) {
            widget.backend.triggerControlEvent(widget.control.id, "close");
          },
          onAdClicked: (Ad ad) {
            widget.backend.triggerControlEvent(widget.control.id, "click");
          },
          onAdWillDismissScreen: (Ad ad) {
            widget.backend
                .triggerControlEvent(widget.control.id, "willDismiss");
          },
          onPaidEvent: (ad, valueMicros, precision, currencyCode) {
            widget.backend.triggerControlEvent(
                widget.control.id,
                "paidEvent",
                jsonEncode({
                  "value_micros": valueMicros,
                  "precision": precision,
                  "currency_code": currencyCode
                }));
          },
          // Called when an impression occurs on the ad.
          onAdImpression: (Ad ad) {
            widget.backend.triggerControlEvent(widget.control.id, "impression");
          },
        ),
      );

      if (!_isLoaded) {
        bannerAd.load();
      }

      return constrainedControl(
          context, AdWidget(ad: bannerAd), widget.parent, widget.control);
    });
  }
}
