import 'dart:typed_data';

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

class ImageControl extends StatefulWidget {
  final Control control;

  static const String svgTag = " xmlns=\"http://www.w3.org/2000/svg\"";

  const ImageControl({
    super.key,
    required this.control,
  });

  @override
  State<ImageControl> createState() => _ImageControlState();
}

class _ImageControlState extends State<ImageControl> {
  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Image.$name($args)");
    switch (name) {
      case "clear_cache":
        imageCache.clear();
      default:
        throw Exception("Unknown Image method: $name");
    }
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Image build: ${widget.control.id}");

    var src = widget.control.getString("src", "")!;
    var srcBase64 = widget.control.getString("src_base64", "")!;
    var srcBytes =
        (widget.control.get("src_bytes") as Uint8List?) ?? Uint8List(0);
    if (src == "" && srcBase64 == "" && srcBytes.isEmpty) {
      return const ErrorControl(
          "Image must have either \"src\" or \"src_base64\" or \"src_bytes\" specified.");
    }
    var errorContent = widget.control.buildWidget("error_content");

    Widget? image = buildImage(
      context: context,
      src: src,
      srcBase64: srcBase64,
      srcBytes: srcBytes,
      width: widget.control.getDouble("width"),
      height: widget.control.getDouble("height"),
      cacheWidth: widget.control.getInt("cache_width"),
      cacheHeight: widget.control.getInt("cache_height"),
      antiAlias: widget.control.getBool("anti_alias", false)!,
      repeat: widget.control.getImageRepeat("repeat", ImageRepeat.noRepeat)!,
      fit: widget.control.getBoxFit("fit"),
      colorBlendMode: widget.control.getBlendMode("color_blend_mode"),
      color: widget.control.getColor("color", context),
      semanticsLabel: widget.control.getString("semantics_label"),
      gaplessPlayback: widget.control.getBool("gapless_playback"),
      excludeFromSemantics:
          widget.control.getBool("exclude_from_semantics", false)!,
      filterQuality: widget.control
          .getFilterQuality("filter_quality", FilterQuality.medium)!,
      disabled: widget.control.disabled,
      errorCtrl: errorContent,
    );
    return LayoutControl(
        control: widget.control,
        child: _clipCorners(
            image, widget.control.getBorderRadius("border_radius")));
  }

  Widget _clipCorners(Widget image, BorderRadius? borderRadius) {
    return borderRadius != null
        ? ClipRRect(borderRadius: borderRadius, child: image)
        : image;
  }
}
