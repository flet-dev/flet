import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

import '../utils/ads.dart';
import '../utils/native.dart';

class NativeAdControl extends StatefulWidget {
  final Control control;

  const NativeAdControl({super.key, required this.control});

  @override
  State<NativeAdControl> createState() => _NativeAdControlState();
}

class _NativeAdControlState extends State<NativeAdControl> with FletStoreMixin {
  bool _isLoaded = false;

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "NativeAd build: ${widget.control.id} (${widget.control.hashCode})");
    final testAdUnitId = isIOSMobile()
        ? 'ca-app-pub-3940256099942544/3986624511'
        : 'ca-app-pub-3940256099942544/2247696110';
    var factoryId = widget.control.getString("factory_id");
    var templateStyle = parseNativeTemplateStyle(
        widget.control.get("template_style"), Theme.of(context));
    if (factoryId == null && templateStyle == null) {
      return const ErrorControl("factory_id or template_style is required");
    }

    NativeAd nativeAd = NativeAd(
        adUnitId: widget.control.getString("unit_id", testAdUnitId)!,
        factoryId: factoryId,
        listener: NativeAdListener(
          onAdLoaded: (ad) {
            widget.control.triggerEvent("load");
            setState(() {
              _isLoaded = true;
            });
          },
          onAdFailedToLoad: (ad, error) {
            widget.control.triggerEvent("error", error.toString());
            ad.dispose(); // Dispose the ad here to free resources
          },
          onAdClicked: (ad) => widget.control.triggerEvent("click"),
          onAdImpression: (ad) => widget.control.triggerEvent("impression"),
          onAdClosed: (ad) => widget.control.triggerEvent("close"),
          onAdOpened: (ad) => widget.control.triggerEvent("open"),
          onAdWillDismissScreen: (ad) =>
              widget.control.triggerEvent("will_dismiss"),
          onPaidEvent: (Ad ad, valueMicros, precision, currencyCode) {
            widget.control.triggerEvent("paid", {
              "value": valueMicros,
              "precision": precision,
              "currency_code": currencyCode
            });
          },
        ),
        request:
            parseAdRequest(widget.control.get("request"), const AdRequest())!,
        nativeTemplateStyle: templateStyle);

    if (!_isLoaded) {
      nativeAd.load();
    }

    return ConstrainedControl(
        control: widget.control, child: AdWidget(ad: nativeAd));
  }
}
