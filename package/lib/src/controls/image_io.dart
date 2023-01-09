import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'dart:io' as io;

SvgPicture getSvgPictureFromFile(
    {required String src,
    required double? width,
    required double? height,
    required BoxFit fit,
    required Color? color,
    required BlendMode blendMode,
    required String? semanticsLabel}) {
  return SvgPicture.file(io.File(src),
      width: width,
      height: height,
      fit: fit,
      color: color,
      colorBlendMode: blendMode,
      semanticsLabel: semanticsLabel);
}
