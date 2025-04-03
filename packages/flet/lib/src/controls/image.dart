import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/images.dart';
import '../widgets/error.dart';
import 'base_controls.dart';
import 'control_widget.dart';

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
    bool disabled = control.disabled || control.parent!.disabled;

    var src = control.getString("src", "")!;
    var srcBase64 = control.getString("srcBase64", "")!;
    if (src == "" && srcBase64 == "") {
      return const ErrorControl(
          "Image must have either \"src\" or \"src_base64\" specified.");
    }
    var errorContentCtrl = control.child("error_content");

    Widget? image = buildImage(
      context: context,
      control: control,
      src: src,
      srcBase64: srcBase64,
      width: control.getDouble("width"),
      height: control.getDouble("height"),
      cacheWidth: control.getInt("cacheWidth"),
      cacheHeight: control.getInt("cacheHeight"),
      antiAlias: control.getBool("antiAlias", false)!,
      repeat:
          parseImageRepeat(control.getString("repeat"), ImageRepeat.noRepeat)!,
      fit: parseBoxFit(control.getString("fit")),
      colorBlendMode: parseBlendMode(control.getString("colorBlendMode")),
      color: control.getColor("color", context),
      semanticsLabel: control.getString("semanticsLabel"),
      gaplessPlayback: control.getBool("gaplessPlayback"),
      excludeFromSemantics: control.getBool("excludeFromSemantics", false)!,
      filterQuality: parseFilterQuality(
          control.getString("filterQuality"), FilterQuality.medium)!,
      disabled: disabled,
      errorCtrl: errorContentCtrl != null
          ? ControlWidget(control: errorContentCtrl)
          : null,
    );
    return ConstrainedControl(
        control: control, child: _clipCorners(image, control));
  }

  Widget _clipCorners(Widget image, Control control) {
    var borderRadius = parseBorderRadius(control, "borderRadius");
    return borderRadius != null
        ? ClipRRect(
            borderRadius: borderRadius,
            child: image,
          )
        : image;
  }
}
