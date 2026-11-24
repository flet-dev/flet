import 'dart:io' as io;

import 'package:flutter/widgets.dart';
import 'package:lottie/lottie.dart';

LottieBuilder fileLottie(
  String path, {
  bool? animate,
  bool? repeat,
  bool? reverse,
  AlignmentGeometry? alignment,
  BoxFit? fit,
  FilterQuality? filterQuality,
  LottieOptions? options,
  bool? backgroundLoading,
  ImageErrorWidgetBuilder? errorBuilder,
  void Function(LottieComposition)? onLoaded,
  void Function(String)? onWarning,
}) =>
    Lottie.file(
      io.File(path),
      animate: animate,
      repeat: repeat,
      reverse: reverse,
      alignment: alignment,
      fit: fit,
      filterQuality: filterQuality,
      options: options,
      backgroundLoading: backgroundLoading,
      errorBuilder: errorBuilder,
      onLoaded: onLoaded,
      onWarning: onWarning,
    );
