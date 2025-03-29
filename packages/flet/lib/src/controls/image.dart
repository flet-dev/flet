import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/images.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_store_mixin.dart';

class ImageControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final List<Control> children;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  static const String svgTag = " xmlns=\"http://www.w3.org/2000/svg\"";

  const ImageControl(
      {super.key,
      required this.parent,
      required this.children,
      required this.control,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("Image build: ${control.id}");
    bool disabled = control.disabled || parentDisabled;

    var src = control.getString("src", "")!;
    var srcBase64 = control.getString("srcBase64", "")!;
    if (src == "" && srcBase64 == "") {
      return const ErrorControl(
          "Image must have either \"src\" or \"src_base64\" specified.");
    }
    var errorContentCtrls =
        children.where((c) => c.name == "error_content" && c.visible);

    return withPageArgs((context, pageArgs) {
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
        repeat: parseImageRepeat(
            control.getString("repeat"), ImageRepeat.noRepeat)!,
        fit: parseBoxFit(control.getString("fit")),
        colorBlendMode: parseBlendMode(control.getString("colorBlendMode")),
        color: control.getColor("color", context),
        semanticsLabel: control.getString("semanticsLabel"),
        gaplessPlayback: control.getBool("gaplessPlayback"),
        excludeFromSemantics: control.getBool("excludeFromSemantics", false)!,
        filterQuality: parseFilterQuality(
            control.getString("filterQuality"), FilterQuality.medium)!,
        disabled: disabled,
        pageArgs: pageArgs,
        errorCtrl: errorContentCtrls.isNotEmpty
            ? createControl(control, errorContentCtrls.first.id, disabled,
                parentAdaptive: control.adaptive ?? parentAdaptive)
            : null,
      );
      return constrainedControl(
          context, _clipCorners(image, control), parent, control);
    });
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
