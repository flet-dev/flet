import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

import '../models/asset_src.dart';
import 'uri.dart';

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

AssetSrc getAssetSrc(String src, Uri pageUri, String assetsDir) {
  var uri = Uri.parse(src);
  return AssetSrc(
      path: uri.hasAuthority ? src : getAssetUri(pageUri, src).toString(),
      isFile: false);
}

ImageProvider getFileImageProvider(String path) {
  throw UnimplementedError();
}
