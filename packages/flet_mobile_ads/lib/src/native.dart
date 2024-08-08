import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

import '../utils/native.dart';

class NativeAdControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const NativeAdControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.backend});

  @override
  State<NativeAdControl> createState() => _NativeAdControlState();
}

class _NativeAdControlState extends State<NativeAdControl> with FletStoreMixin {
  NativeAd? _nativeAd;
  bool _isLoaded = false;

  void loadAd() {
    _nativeAd = NativeAd(
        adUnitId: widget.control
            .attrString("unitId", 'ca-app-pub-3940256099942544/2247696110')!,
        listener: NativeAdListener(
          onAdLoaded: (ad) {
            debugPrint('$NativeAd loaded.');
            widget.backend.triggerControlEvent(widget.control.id, "load");
            setState(() {
              _isLoaded = true;
            });
          },
          onAdFailedToLoad: (ad, error) {
            widget.backend.triggerControlEvent(
                widget.control.id, "error", error.toString());
            // Dispose the ad here to free resources.
            debugPrint('$NativeAd failedToLoad: $error');
            ad.dispose();
          },
          onAdClicked: (ad) {
            widget.backend.triggerControlEvent(widget.control.id, "click");
          },
          onAdImpression: (ad) {
            widget.backend.triggerControlEvent(widget.control.id, "impression");
          },
          onAdClosed: (ad) {
            widget.backend.triggerControlEvent(widget.control.id, "close");
          },
          onAdOpened: (ad) {
            widget.backend.triggerControlEvent(widget.control.id, "open");
          },
          onAdWillDismissScreen: (ad) {
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
        ),
        request: const AdRequest(),
        nativeTemplateStyle: parseNativeTemplateStyle(
            Theme.of(context), widget.control, "nativeTemplateStyle"))
      ..load();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "NativeAd build: ${widget.control.id} (${widget.control.hashCode})");
    return withPagePlatform((context, platform) {
      final testAdUnitId = platform == TargetPlatform.iOS
          ? 'ca-app-pub-3940256099942544/3986624511'
          : 'ca-app-pub-3940256099942544/2247696110';
      var factoryId = widget.control.attrString("factoryId");
      var nativeTemplateStyle = parseNativeTemplateStyle(
          Theme.of(context), widget.control, "templateStyle");
      if (factoryId == null && nativeTemplateStyle == null) {
        return const ErrorControl(
            "factory_id or native_template_style is required");
      }

      NativeAd nativeAd = NativeAd(
          adUnitId: widget.control.attrString("unitId", testAdUnitId)!,
          factoryId: factoryId,
          listener: NativeAdListener(
            onAdLoaded: (ad) {
              debugPrint('$NativeAd loaded.');
              widget.backend.triggerControlEvent(widget.control.id, "load");
              setState(() {
                _isLoaded = true;
              });
            },
            onAdFailedToLoad: (ad, error) {
              widget.backend.triggerControlEvent(
                  widget.control.id, "error", error.toString());
              // Dispose the ad here to free resources.
              debugPrint('$NativeAd failedToLoad: $error');
              ad.dispose();
            },
            onAdClicked: (ad) {
              widget.backend.triggerControlEvent(widget.control.id, "click");
            },
            onAdImpression: (ad) {
              widget.backend
                  .triggerControlEvent(widget.control.id, "impression");
            },
            onAdClosed: (ad) {
              widget.backend.triggerControlEvent(widget.control.id, "close");
            },
            onAdOpened: (ad) {
              widget.backend.triggerControlEvent(widget.control.id, "open");
            },
            onAdWillDismissScreen: (ad) {
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
          ),
          request: const AdRequest(),
          nativeTemplateStyle: nativeTemplateStyle);

      if (!_isLoaded) {
        nativeAd.load();
      }

      return constrainedControl(
          context, AdWidget(ad: nativeAd), widget.parent, widget.control);
    });
  }
}
