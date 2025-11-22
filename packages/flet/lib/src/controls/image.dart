import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/colors.dart';
import '../utils/images.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class ImageControl extends StatelessWidget {
  final Control control;

  static const String svgTag = " xmlns=\"http://www.w3.org/2000/svg\"";

  const ImageControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("Image build: ${control.id}");

    var rawSrc = control.get("src");
    if (rawSrc == null) {
      return const ErrorControl("Image must have \"src\" specified.");
    }

    Widget? image = buildImage(
      context: context,
      src: rawSrc,
      width: control.getDouble("width"),
      height: control.getDouble("height"),
      cacheWidth: control.getInt("cache_width"),
      cacheHeight: control.getInt("cache_height"),
      antiAlias: control.getBool("anti_alias", false)!,
      repeat: control.getImageRepeat("repeat", ImageRepeat.noRepeat)!,
      fit: control.getBoxFit("fit"),
      colorBlendMode: control.getBlendMode("color_blend_mode"),
      color: control.getColor("color", context),
      semanticsLabel: control.getString("semantics_label"),
      gaplessPlayback: control.getBool("gapless_playback"),
      excludeFromSemantics: control.getBool("exclude_from_semantics", false)!,
      filterQuality:
          control.getFilterQuality("filter_quality", FilterQuality.medium)!,
      disabled: control.disabled,
      errorCtrl: control.buildWidget("error_content"),
    );
    return LayoutControl(
        control: control,
        child: _clipCorners(image, control.getBorderRadius("border_radius")));
  }

  Widget _clipCorners(Widget image, BorderRadius? borderRadius) {
    return borderRadius != null
        ? ClipRRect(borderRadius: borderRadius, child: image)
        : image;
  }
}
