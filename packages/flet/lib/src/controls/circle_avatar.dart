import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class CircleAvatarControl extends StatelessWidget {
  final Control control;

  const CircleAvatarControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("CircleAvatar build: ${control.id}");

    var foregroundImageSrc = control.getString("foreground_image_src");
    var backgroundImageSrc = control.getString("background_image_src");
    var content = control.buildTextOrWidget("content");

    ImageProvider<Object>? backgroundImage;
    ImageProvider<Object>? foregroundImage;

    if (foregroundImageSrc != null || backgroundImageSrc != null) {
      var assetSrc = control.backend
          .getAssetSource((foregroundImageSrc ?? backgroundImageSrc)!);

      // foregroundImage
      if (foregroundImageSrc != null) {
        if (assetSrc.isFile) {
          // from File
          foregroundImage = AssetImage(assetSrc.path);
        } else {
          // URL
          foregroundImage = NetworkImage(assetSrc.path);
        }
      }

      // backgroundImage
      if (backgroundImageSrc != null) {
        if (assetSrc.isFile) {
          // from File
          backgroundImage = AssetImage(assetSrc.path);
        } else {
          // URL
          backgroundImage = NetworkImage(assetSrc.path);
        }
      }
    }

    var avatar = CircleAvatar(
        foregroundImage: foregroundImage,
        backgroundImage: backgroundImage,
        backgroundColor: control.getColor("bgcolor", context),
        foregroundColor: control.getColor("color", context),
        radius: control.getDouble("radius"),
        minRadius: control.getDouble("min_radius"),
        maxRadius: control.getDouble("max_radius"),
        onBackgroundImageError: backgroundImage != null
            ? (object, trace) {
                control.triggerEvent("image_error", "background");
              }
            : null,
        onForegroundImageError: foregroundImage != null
            ? (object, trace) {
                control.triggerEvent("image_error", "foreground");
              }
            : null,
        child: content);

    return LayoutControl(control: control, child: avatar);
  }
}
