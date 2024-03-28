import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/images.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

class CircleAvatarControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const CircleAvatarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("CircleAvatar build: ${control.id}");
    bool disabled = control.isDisabled || parentDisabled;

    return withPageArgs((context, pageArgs) {
      // DEPRECATED: foregroundImageUrl and backgroundImageUrl
      var foregroundImageSrc = control.attrString("foregroundImageSrc") ??
          control.attrString("foregroundImageUrl");
      var backgroundImageSrc = control.attrString("backgroundImageSrc") ??
          control.attrString("backgroundImageUrl");
      var contentCtrls = children.where((c) => c.name == "content");

      ImageProvider<Object>? backgroundImage;
      ImageProvider<Object>? foregroundImage;

      if (foregroundImageSrc != null || backgroundImageSrc != null) {
        var assetSrc = getAssetSrc((foregroundImageSrc ?? backgroundImageSrc)!,
            pageArgs.pageUri!, pageArgs.assetsDir);

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
          backgroundColor: control.attrColor("bgColor", context),
          foregroundColor: control.attrColor("color", context),
          radius: control.attrDouble("radius"),
          minRadius: control.attrDouble("minRadius"),
          maxRadius: control.attrDouble("maxRadius"),
          onBackgroundImageError: backgroundImage != null
              ? (object, trace) {
                  backend.triggerControlEvent(
                      control.id, "imageError", "background");
                }
              : null,
          onForegroundImageError: foregroundImage != null
              ? (object, trace) {
                  backend.triggerControlEvent(
                      control.id, "imageError", "foreground");
                }
              : null,
          child: contentCtrls.isNotEmpty
              ? createControl(control, contentCtrls.first.id, disabled)
              : null);

      return constrainedControl(context, avatar, parent, control);
    });
  }
}
