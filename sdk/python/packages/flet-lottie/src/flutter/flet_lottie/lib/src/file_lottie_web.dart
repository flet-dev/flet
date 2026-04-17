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
}) {
  // Local file loading is not supported on web. On web, `getAssetSrc`
  // always returns `isFile: false`, so this code path is unreachable at
  // runtime — this stub exists only to keep the package compiling for web.
  throw UnsupportedError(
    'Lottie.file is not supported on Flutter Web.',
  );
}
