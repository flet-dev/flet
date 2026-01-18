import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/images.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class ImageControl extends StatelessWidget {
  final Control control;

  static const String svgTag = " xmlns=\"http://www.w3.org/2000/svg\"";

  const ImageControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Image build: ${control.id}");

    var rawSrc = control.get("src");
    if (rawSrc == null) {
      return const ErrorControl("Image must have \"src\" specified.");
    }

    final width = control.getDouble("width");
    final height = control.getDouble("height");
    final fit = control.getBoxFit("fit");
    final repeat = control.getImageRepeat("repeat", ImageRepeat.noRepeat)!;
    final color = control.getColor("color", context);
    final colorBlendMode = control.getBlendMode("color_blend_mode");
    final semanticsLabel = control.getString("semantics_label");
    final gaplessPlayback = control.getBool("gapless_playback");
    final excludeFromSemantics =
        control.getBool("exclude_from_semantics", false)!;
    final filterQuality =
        control.getFilterQuality("filter_quality", FilterQuality.medium)!;
    final cacheWidth = control.getInt("cache_width");
    final cacheHeight = control.getInt("cache_height");
    final antiAlias = control.getBool("anti_alias", false)!;
    final errorContent = control.buildWidget("error_content");

    // Optional placeholder shown while the image is loading.
    Widget? placeholder;
    final placeholderSrc = control.get("placeholder_src");
    if (placeholderSrc != null) {
      placeholder = buildImage(
        context: context,
        src: placeholderSrc,
        width: width,
        height: height,
        fit: control.getBoxFit("placeholder_fit", fit),
        repeat: repeat,
        color: color,
        colorBlendMode: colorBlendMode,
        semanticsLabel: semanticsLabel,
        gaplessPlayback: gaplessPlayback,
        excludeFromSemantics: excludeFromSemantics,
        filterQuality: filterQuality,
        cacheWidth: cacheWidth,
        cacheHeight: cacheHeight,
        antiAlias: antiAlias,
        errorCtrl: errorContent,
      );
    }

    final fadeConfig = ImageFadeConfig(
        placeholder: placeholder,
        fadeInAnimation: control.getAnimation("fade_in_animation"),
        placeholderFadeOutAnimation:
            control.getAnimation("placeholder_fade_out_animation"));

    Widget? image = buildImage(
      context: context,
      src: rawSrc,
      width: width,
      height: height,
      cacheWidth: cacheWidth,
      cacheHeight: cacheHeight,
      antiAlias: antiAlias,
      repeat: repeat,
      fit: fit,
      colorBlendMode: colorBlendMode,
      color: color,
      semanticsLabel: semanticsLabel,
      gaplessPlayback: gaplessPlayback,
      excludeFromSemantics: excludeFromSemantics,
      filterQuality: filterQuality,
      disabled: control.disabled,
      errorCtrl: errorContent,
      fadeConfig: fadeConfig.enabled ? fadeConfig : null,
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
