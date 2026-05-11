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
  // Pass through any value that already carries a URL scheme (http, https,
  // data, blob, file, rtsp, rtmp, srt, udp, ...). Single-letter schemes are
  // ignored so Windows-style "C:\..." paths fall into the relative branch.
  final parsed = Uri.tryParse(src);
  if (parsed != null && parsed.scheme.length > 1) {
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
