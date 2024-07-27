import 'dart:convert';
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

bool isBase64ImageString(String s) {
  // Check for base64 prefix
  final base64PrefixPattern = RegExp(r'^data:image\/[a-zA-Z]+;base64,');
  if (base64PrefixPattern.hasMatch(s)) {
    return true;
  }

  // Check if string contains only valid base64 characters and has a valid length (multiple of 4)
  final base64CharPattern = RegExp(r'^[A-Za-z0-9+/=]+$');
  if (base64CharPattern.hasMatch(s) && s.length % 4 == 0) {
    try {
      base64.decode(s);
      return true;
    } catch (e) {
      return false;
    }
  }

  return false;
}

bool isUrlOrPath(String s) {
  // Check for URL pattern
  final urlPattern = RegExp(r'^(http:\/\/|https:\/\/|www\.)');
  if (urlPattern.hasMatch(s)) {
    return true;
  }

  // Check for common file path characters
  final filePathPattern = RegExp(r'^[a-zA-Z0-9_\-/\\\.]+$');
  if (filePathPattern.hasMatch(s)) {
    return true;
  }

  return false;
}
