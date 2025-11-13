import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class CircleAvatarControl extends StatelessWidget {
  final Control control;

  const CircleAvatarControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("CircleAvatar build: ${control.id}");

    var foregroundImage =
        getImageProvider(context, control.get("foreground_image_src"));
    var backgroundImage =
        getImageProvider(context, control.get("background_image_src"));

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
        child: control.buildTextOrWidget("content"));

    return LayoutControl(control: control, child: avatar);
  }
}
