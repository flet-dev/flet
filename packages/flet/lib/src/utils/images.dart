import 'dart:convert';
import 'dart:io' as io;
import 'dart:typed_data';
import 'dart:ui';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/strings.dart';
import '../utils/uri.dart';
import '../widgets/error.dart';
import 'collections.dart';
import 'colors.dart';
import 'gradient.dart';
import 'images.dart';
import 'numbers.dart';

export "images_web.dart" if (dart.library.io) 'images_io.dart';

ImageRepeat? parseImageRepeat(String? value, [ImageRepeat? defaultValue]) {
  if (value == null) return defaultValue;
  return ImageRepeat.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

BlendMode? parseBlendMode(String? value, [BlendMode? defaultValue]) {
  if (value == null) return defaultValue;
  return BlendMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

BoxFit? parseBoxFit(String? value, [BoxFit? defaultValue]) {
  if (value == null) return defaultValue;
  return BoxFit.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

ImageFilter? parseBlur(dynamic value, [ImageFilter? defaultValue]) {
  if (value == null) return defaultValue;

  double sigmaX = 0.0, sigmaY = 0.0;
  TileMode? tileMode;
  if (value is num) {
    sigmaX = sigmaY = parseDouble(value, 0)!;
  } else if (value is List) {
    sigmaX = parseDouble(value.isNotEmpty ? value[0] : 0, 0)!;
    sigmaY = parseDouble(value.length > 1 ? value[1] : value[0], 0)!;
  } else if (value is Map) {
    sigmaX = parseDouble(value["sigma_x"], 0)!;
    sigmaY = parseDouble(value["sigma_y"], 0)!;
    tileMode = parseTileMode(value["tile_mode"]);
  }

  return ImageFilter.blur(sigmaX: sigmaX, sigmaY: sigmaY, tileMode: tileMode);
}

ColorFilter? parseColorFilter(dynamic value, ThemeData theme,
    [ColorFilter? defaultValue]) {
  if (value == null) return defaultValue;
  Color? color = parseColor(value["color"], theme);
  BlendMode? blendMode = parseBlendMode(value["blend_mode"]);
  if (color == null || blendMode == null) return defaultValue;
  return ColorFilter.mode(color, blendMode);
}

FilterQuality? parseFilterQuality(String? value,
    [FilterQuality? defaultValue]) {
  if (value == null) return defaultValue;
  return FilterQuality.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

/// Returns a Flutter [ImageProvider]
/// for anything supported by [ResolvedAssetSource].
ImageProvider? parseImageProvider(dynamic src, BuildContext context) {
  final resolvedSrc =
      src is ResolvedAssetSource ? src : ResolvedAssetSource.from(src);

  if (resolvedSrc.error != null) {
    debugPrint("getImageProvider failed decoding src: ${resolvedSrc.error}");
    return null;
  }

  // bytes
  if (resolvedSrc.hasBytes) {
    try {
      return MemoryImage(resolvedSrc.bytes!);
    } catch (ex) {
      debugPrint("getImageProvider failed decoding bytes");
      return null;
    }
  }

  // URL or asset path
  if (resolvedSrc.hasUri) {
    var assetSrc = FletBackend.of(context).getAssetSource(resolvedSrc.uri!);
    return assetSrc.isFile
        ? getFileImageProvider(assetSrc.path)
        : NetworkImage(assetSrc.path);
  }

  return null;
}

/// Builds the correct image widget ([Image] or [SvgPicture])
/// for any supported `src`.
Widget buildImage({
  required BuildContext context,
  required Widget? errorCtrl,
  required dynamic src,
  double? width,
  double? height,
  ImageRepeat repeat = ImageRepeat.noRepeat,
  BoxFit? fit,
  BlendMode? colorBlendMode,
  Color? color,
  String? semanticsLabel,
  bool? gaplessPlayback,
  int? cacheWidth,
  int? cacheHeight,
  bool antiAlias = false,
  bool excludeFromSemantics = false,
  FilterQuality filterQuality = FilterQuality.low,
  bool disabled = false,
}) {
  const String svgTag = " xmlns=\"http://www.w3.org/2000/svg\"";

  final resolvedSrc = ResolvedAssetSource.from(src);
  if (resolvedSrc.error != null) {
    return errorCtrl ??
        ErrorControl("Error decoding src", description: resolvedSrc.error);
  }

  if (resolvedSrc.hasBytes) {
    Uint8List bytes = resolvedSrc.bytes!;
    try {
      // SVG bytes
      if (arrayIndexOf(bytes, Uint8List.fromList(utf8.encode(svgTag))) != -1) {
        return SvgPicture.memory(bytes,
            width: width,
            height: height,
            excludeFromSemantics: excludeFromSemantics,
            fit: fit ?? BoxFit.contain,
            colorFilter: color != null
                ? ColorFilter.mode(color, colorBlendMode ?? BlendMode.srcIn)
                : null,
            semanticsLabel: semanticsLabel);
      } else {
        // other image bytes
        return Image.memory(bytes,
            width: width,
            height: height,
            repeat: repeat,
            fit: fit,
            color: color,
            cacheHeight: cacheHeight,
            cacheWidth: cacheWidth,
            filterQuality: filterQuality,
            isAntiAlias: antiAlias,
            colorBlendMode: colorBlendMode,
            gaplessPlayback: gaplessPlayback ?? false,
            excludeFromSemantics: excludeFromSemantics,
            semanticLabel: semanticsLabel);
      }
    } catch (ex) {
      return ErrorControl("Error decoding base64: ${ex.toString()}");
    }
  } else if (resolvedSrc.hasUri) {
    var stringSrc = resolvedSrc.uri!;
    if (stringSrc.contains(svgTag)) {
      return SvgPicture.memory(Uint8List.fromList(utf8.encode(stringSrc)),
          width: width,
          height: height,
          fit: fit ?? BoxFit.contain,
          excludeFromSemantics: excludeFromSemantics,
          colorFilter: color != null
              ? ColorFilter.mode(color, colorBlendMode ?? BlendMode.srcIn)
              : null,
          semanticsLabel: semanticsLabel);
    } else {
      var assetSrc = FletBackend.of(context).getAssetSource(stringSrc);
      if (assetSrc.isFile) {
        // SVG File
        if (assetSrc.path.endsWith(".svg")) {
          return getSvgPictureFromFile(
              src: assetSrc.path,
              width: width,
              height: height,
              fit: fit ?? BoxFit.contain,
              color: color,
              blendMode: colorBlendMode ?? BlendMode.srcIn,
              semanticsLabel: semanticsLabel);
        } else {
          // other image File
          return Image.file(
            io.File(assetSrc.path),
            width: width,
            height: height,
            repeat: repeat,
            filterQuality: filterQuality,
            excludeFromSemantics: excludeFromSemantics,
            fit: fit,
            color: color,
            isAntiAlias: antiAlias,
            cacheHeight: cacheHeight,
            cacheWidth: cacheWidth,
            gaplessPlayback: gaplessPlayback ?? false,
            colorBlendMode: colorBlendMode,
            semanticLabel: semanticsLabel,
            errorBuilder: errorCtrl != null
                ? (context, error, stackTrace) {
                    return errorCtrl;
                  }
                : null,
          );
        }
      } else {
        // SVG URL
        if (assetSrc.path.endsWith(".svg")) {
          return SvgPicture.network(
            assetSrc.path,
            width: width,
            height: height,
            excludeFromSemantics: excludeFromSemantics,
            fit: fit ?? BoxFit.contain,
            colorFilter: color != null
                ? ColorFilter.mode(color, colorBlendMode ?? BlendMode.srcIn)
                : null,
            semanticsLabel: semanticsLabel,
          );
        } else {
          // other image URL
          return Image.network(
            assetSrc.path,
            width: width,
            height: height,
            repeat: repeat,
            filterQuality: filterQuality,
            cacheHeight: cacheHeight,
            cacheWidth: cacheWidth,
            isAntiAlias: antiAlias,
            excludeFromSemantics: excludeFromSemantics,
            fit: fit,
            color: color,
            gaplessPlayback: gaplessPlayback ?? false,
            colorBlendMode: colorBlendMode,
            semanticLabel: semanticsLabel,
            errorBuilder: errorCtrl != null
                ? (context, error, stackTrace) {
                    return errorCtrl;
                  }
                : null,
          );
        }
      }
    }
  }

  return const ErrorControl("A valid src value must be specified.");
}

class ResolvedAssetSource {
  const ResolvedAssetSource({this.bytes, this.uri, this.error});

  /// Raw bytes (ex: base64-decoded payload).
  final Uint8List? bytes;

  /// String representation (ex: URL, asset path).
  final String? uri;

  /// Optional error message describing a resolution failure.
  final String? error;

  /// True if the instance contains non-empty bytes.
  bool get hasBytes => bytes != null && bytes!.isNotEmpty;

  /// True if the instance contains a non-empty string value.
  bool get hasUri => uri != null && uri!.isNotEmpty;

  /// True if both bytes and string are missing or empty.
  bool get isEmpty => !hasBytes && !hasUri;

  /// Factory that normalizes any supported image source into
  /// a [ResolvedAssetSource].
  ///
  /// Supports:
  /// - `Uint8List`, `List<int>` → interpreted as raw bytes
  /// - `String` → URL, asset path, or Base64-encoded data
  factory ResolvedAssetSource.from(dynamic src) {
    // bytes
    final listBytes = _bytesFromList(src);
    if (listBytes != null) {
      return listBytes.isEmpty
          ? const ResolvedAssetSource()
          : ResolvedAssetSource(bytes: listBytes);
    }

    // string sources
    if (src is String) {
      src = src.trim();

      // empty string
      if (src.isEmpty) return const ResolvedAssetSource();

      // URL
      if (isUrl(src)) return ResolvedAssetSource(uri: src);

      // asset path
      if (src.contains(".")) return ResolvedAssetSource(uri: src);

      // Base64
      try {
        final srcAsBytes = base64.decode(src.stripBase64DataHeader());
        return ResolvedAssetSource(bytes: srcAsBytes);
      } catch (_) {}

      // asset path
      return ResolvedAssetSource(uri: src);
    }

    // unknown or unsupported source type
    return ResolvedAssetSource(
        error: "${src.runtimeType} is not a supported source type.");
  }
}

/// Converts various list-like inputs into a Uint8List,
/// or returns null if unsupported.
Uint8List? _bytesFromList(dynamic value) {
  if (value is Uint8List) {
    return value;
  } else if (value is List<int>) {
    return Uint8List.fromList(value);
  } else if (value is List && value.every((e) => e is int)) {
    return Uint8List.fromList(value.cast<int>());
  }

  return null;
}

bool isFilePath(String value) {
  final filePathPattern = RegExp(r'^[a-zA-Z0-9_\-/\\\.]+$');
  return filePathPattern.hasMatch(value);
}

extension ImageParsers on Control {
  ImageRepeat? getImageRepeat(String propertyName,
      [ImageRepeat? defaultValue]) {
    return parseImageRepeat(get(propertyName), defaultValue);
  }

  BlendMode? getBlendMode(String propertyName, [BlendMode? defaultValue]) {
    return parseBlendMode(get(propertyName), defaultValue);
  }

  BoxFit? getBoxFit(String propertyName, [BoxFit? defaultValue]) {
    return parseBoxFit(get(propertyName), defaultValue);
  }

  ImageFilter? getBlur(String propertyName, [ImageFilter? defaultValue]) {
    return parseBlur(get(propertyName), defaultValue);
  }

  ColorFilter? getColorFilter(String propertyName, ThemeData theme,
      [ColorFilter? defaultValue]) {
    return parseColorFilter(get(propertyName), theme, defaultValue);
  }

  FilterQuality? getFilterQuality(String propertyName,
      [FilterQuality? defaultValue]) {
    return parseFilterQuality(get(propertyName), defaultValue);
  }

  ResolvedAssetSource getSrc(String propertyName) {
    return ResolvedAssetSource.from(get(propertyName));
  }

  ImageProvider? getImageProvider(String propertyName, BuildContext context) {
    return parseImageProvider(get(propertyName), context);
  }
}
