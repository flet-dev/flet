import 'dart:io' as io;

import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:path/path.dart' as p;

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
  return SvgPicture.file(io.File(src),
      width: width,
      height: height,
      fit: fit,
      colorFilter: color != null ? ColorFilter.mode(color, blendMode) : null,
      semanticsLabel: semanticsLabel);
}

AssetSrc getAssetSrc(String src, Uri pageUri, String assetsDir) {
  if (src.startsWith("http://") || src.startsWith("https://")) {
    return AssetSrc(path: src, isFile: false);
  } else if (io.File(src).existsSync()) {
    return AssetSrc(path: src, isFile: true);
  } else if (assetsDir != "") {
    var filePath = normalizePath(src);
    if (filePath.startsWith(p.separator)) {
      filePath = filePath.substring(1);
    }
    return AssetSrc(
        path: p.join(normalizePath(assetsDir), filePath), isFile: true);
  } else {
    var uri = Uri.parse(src);
    return AssetSrc(
        path: uri.hasAuthority ? src : getAssetUri(pageUri, src).toString(),
        isFile: false);
  }
}

ImageProvider getFileImageProvider(String path) {
  return FileImage(io.File(path));
}

String normalizePath(String path) {
  return path.replaceAll(RegExp(r'[\\/]'), p.separator);
}
