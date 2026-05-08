import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

import '../models/asset_source.dart';

SvgPicture getSvgPictureFromFile(
    {required String src,
    required double? width,
    required double? height,
    required BoxFit fit,
    required Color? color,
    required BlendMode blendMode,
    required String? semanticsLabel}) {
  return SvgPicture.string("<svg/>");
}

AssetSource getAssetSrc(String src, Uri pageUri, String assetsDir) {
  if (src.startsWith("http://") ||
      src.startsWith("https://") ||
      src.startsWith("data:") ||
      src.startsWith("blob:")) {
    return AssetSource(path: src, isFile: false);
  }
  if (assetsDir.isNotEmpty) {
    final cleaned = src.startsWith("/") ? src.substring(1) : src;
    final base = assetsDir.endsWith("/") ? assetsDir : "$assetsDir/";
    return AssetSource(path: "$base$cleaned", isFile: false);
  }
  return AssetSource(path: src, isFile: false);
}

ImageProvider getFileImageProvider(String path) {
  throw UnimplementedError();
}
