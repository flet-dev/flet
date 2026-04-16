import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';

import 'utils/map.dart';

class OverlayImageLayerControl extends StatelessWidget {
  final Control control;

  const OverlayImageLayerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("OverlayImageLayerControl build: ${control.id}");

    final overlayImages = control
        .children("overlay_images")
        .map((overlayImage) {
          overlayImage.notifyParent = true;

          final imageProvider = overlayImage.getImageProvider("src", context);
          if (imageProvider == null) return null;

          final opacity = overlayImage.getDouble("opacity", 1.0)!;
          final gaplessPlayback =
              overlayImage.getBool("gapless_playback", false)!;
          final filterQuality = overlayImage.getFilterQuality(
              "filter_quality", FilterQuality.medium)!;

          switch (overlayImage.type) {
            case "OverlayImage":
              final bounds = overlayImage.getLatLngBounds("bounds");
              if (bounds == null) return null;
              return OverlayImage(
                imageProvider: imageProvider,
                bounds: bounds,
                opacity: opacity,
                gaplessPlayback: gaplessPlayback,
                filterQuality: filterQuality,
              );
            case "RotatedOverlayImage":
              final topLeftCorner = overlayImage.getLatLng("top_left_corner");
              final bottomLeftCorner =
                  overlayImage.getLatLng("bottom_left_corner");
              final bottomRightCorner =
                  overlayImage.getLatLng("bottom_right_corner");
              if (topLeftCorner == null ||
                  bottomLeftCorner == null ||
                  bottomRightCorner == null) {
                return null;
              }
              return RotatedOverlayImage(
                imageProvider: imageProvider,
                topLeftCorner: topLeftCorner,
                bottomLeftCorner: bottomLeftCorner,
                bottomRightCorner: bottomRightCorner,
                opacity: opacity,
                gaplessPlayback: gaplessPlayback,
                filterQuality: filterQuality,
              );
            default:
              return null;
          }
        })
        .nonNulls
        .toList();

    return BaseControl(
      control: control,
      child: OverlayImageLayer(overlayImages: overlayImages),
    );
  }
}
