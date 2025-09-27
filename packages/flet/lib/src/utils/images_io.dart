import 'dart:io' as io;

import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:path/path.dart' as p;

import '../models/asset_source.dart';
import 'lru_cache.dart';
import 'uri.dart';

String _fileKey(String path) {
  // absolute + normalized; case-insensitive on Windows
  final abs = io.File(path).absolute.path;
  final norm = p.normalize(abs);
  return io.Platform.isWindows ? norm.toLowerCase() : norm;
}

class _FileLru {
  _FileLru({this.capacity = 512})
      : _cache = LruCache<String, io.File>(capacity);
  final int capacity;
  final LruCache<String, io.File> _cache;

  io.File get(String path) {
    final key = _fileKey(path);
    final cached = _cache.get(key);
    if (cached != null) return cached;
    final f = io.File(key); // already absolute/normalized
    _cache.set(key, f);
    return f;
  }
}

final _fileLru = _FileLru(capacity: 1024);

SvgPicture getSvgPictureFromFile(
    {required String src,
    required double? width,
    required double? height,
    required BoxFit fit,
    required Color? color,
    required BlendMode blendMode,
    required String? semanticsLabel}) {
  final file = _fileLru.get(src);
  return SvgPicture.file(file,
      width: width,
      height: height,
      fit: fit,
      colorFilter: color != null ? ColorFilter.mode(color, blendMode) : null,
      semanticsLabel: semanticsLabel);
}

AssetSource getAssetSrc(String src, Uri pageUri, String assetsDir) {
  if (src.startsWith("http://") || src.startsWith("https://")) {
    return AssetSource(path: src, isFile: false);
  } else if (io.File(src).existsSync()) {
    return AssetSource(path: src, isFile: true);
  } else if (assetsDir != "") {
    var filePath = normalizePath(src);
    if (filePath.startsWith(p.separator)) {
      filePath = filePath.substring(1);
    }
    return AssetSource(
        path: p.join(normalizePath(assetsDir), filePath), isFile: true);
  } else {
    var uri = Uri.parse(src);
    return AssetSource(
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
