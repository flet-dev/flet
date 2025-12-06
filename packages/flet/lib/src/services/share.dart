import 'dart:ui';

import 'package:flutter/foundation.dart';
import 'package:path/path.dart' as p;
import 'package:share_plus/share_plus.dart';

import '../flet_service.dart';
import '../utils/numbers.dart';

class ShareService extends FletService {
  ShareService({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("ShareService(${control.id}).init");
    control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    switch (name) {
      case "share_text":
        return _share(
          text: args["text"],
          title: args["title"],
          subject: args["subject"],
          previewThumbnail: _parseShareFile(args["preview_thumbnail"]),
          sharePositionOrigin: _parseRect(args["share_position_origin"]),
          downloadFallbackEnabled:
              parseBool(args["download_fallback_enabled"], true) ?? true,
          mailToFallbackEnabled:
              parseBool(args["mail_to_fallback_enabled"], true) ?? true,
          excludedCupertinoActivities: _parseCupertinoActivityTypes(
              args["excluded_cupertino_activities"]),
        );
      case "share_uri":
        return _share(
          uri: args["uri"],
          sharePositionOrigin: _parseRect(args["share_position_origin"]),
          excludedCupertinoActivities: _parseCupertinoActivityTypes(
              args["excluded_cupertino_activities"]),
        );
      case "share_files":
        return _share(
          files: _parseShareFiles(args["files"]),
          title: args["title"],
          text: args["text"],
          subject: args["subject"],
          previewThumbnail: _parseShareFile(args["preview_thumbnail"]),
          sharePositionOrigin: _parseRect(args["share_position_origin"]),
          downloadFallbackEnabled:
              parseBool(args["download_fallback_enabled"], true) ?? true,
          mailToFallbackEnabled:
              parseBool(args["mail_to_fallback_enabled"], true) ?? true,
          excludedCupertinoActivities: _parseCupertinoActivityTypes(
              args["excluded_cupertino_activities"]),
          fileNameOverrides: _parseFileNameOverrides(args["files"]),
        );
      default:
        throw Exception("Unknown Share method: $name");
    }
  }

  Future<Map<String, dynamic>> _share({
    String? text,
    String? title,
    String? subject,
    String? uri,
    List<XFile>? files,
    XFile? previewThumbnail,
    Rect? sharePositionOrigin,
    bool downloadFallbackEnabled = true,
    bool mailToFallbackEnabled = true,
    List<CupertinoActivityType>? excludedCupertinoActivities,
    List<String>? fileNameOverrides,
  }) async {
    final params = ShareParams(
        text: text,
        title: title,
        subject: subject,
        uri: uri != null ? Uri.parse(uri) : null,
        files: files,
        previewThumbnail: previewThumbnail,
        sharePositionOrigin: sharePositionOrigin,
        downloadFallbackEnabled: downloadFallbackEnabled,
        mailToFallbackEnabled: mailToFallbackEnabled,
        excludedCupertinoActivities: excludedCupertinoActivities,
        fileNameOverrides: fileNameOverrides);

    final result = await SharePlus.instance.share(params);
    return {"status": result.status.name, "raw": result.raw};
  }

  List<XFile>? _parseShareFiles(dynamic value) {
    if (value is List) {
      return value.map((e) => _parseShareFile(e)!).toList();
    }
    return null;
  }

  List<String>? _parseFileNameOverrides(dynamic value) {
    if (value is List) {
      final names = value.map((e) => _extractFileName(e)).toList();
      return names.isEmpty ? null : names;
    }
    return null;
  }

  String _extractFileName(dynamic value) {
    if (value is Map) {
      final name = (value["name"] as String?)?.trim();
      if (name != null && name.isNotEmpty) {
        return name;
      }
      final path = (value["path"] as String?)?.trim();
      if (path != null && path.isNotEmpty) {
        final base = p.basename(path);
        if (base.isNotEmpty) {
          return base;
        }
      }
    }
    return "shared_file";
  }

  XFile? _parseShareFile(dynamic value) {
    if (value is Map) {
      final path = value["path"] as String?;
      final data = value["data"];
      final mimeType = value["mime_type"] as String?;
      final name = value["name"] as String?;

      if (path != null) {
        final resolvedName = (name ?? p.basename(path)).trim().isNotEmpty
            ? (name ?? p.basename(path)).trim()
            : "shared_file";
        return XFile(path, name: resolvedName);
      }

      if (data != null) {
        Uint8List bytes;
        if (data is Uint8List) {
          bytes = data;
        } else if (data is List<int>) {
          bytes = Uint8List.fromList(data);
        } else {
          throw ArgumentError("data must be Uint8List or List<int>");
        }
        final resolvedName =
            name != null && name.isNotEmpty ? name : "shared_file";
        return XFile.fromData(bytes, mimeType: mimeType, name: resolvedName);
      }
    }
    return null;
  }

  Rect? _parseRect(dynamic value) {
    if (value is Map) {
      final x = parseDouble(value["x"], 0) ?? 0;
      final y = parseDouble(value["y"], 0) ?? 0;
      final width = parseDouble(value["width"], 0) ?? 0;
      final height = parseDouble(value["height"], 0) ?? 0;
      return Rect.fromLTWH(x, y, width, height);
    }
    return null;
  }

  List<CupertinoActivityType>? _parseCupertinoActivityTypes(dynamic value) {
    if (value is List) {
      final types = <CupertinoActivityType>[];
      for (final v in value) {
        try {
          final match = CupertinoActivityType.values
              .firstWhere((e) => e.name == v || e.value == v);
          types.add(match);
        } catch (_) {}
      }
      return types.isEmpty ? null : types;
    }
    return null;
  }

  @override
  void dispose() {
    debugPrint("ShareService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
