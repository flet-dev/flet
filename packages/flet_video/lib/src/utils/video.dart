import 'dart:convert';
import 'dart:io';

import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';

List<Media> parseVideoMedia(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return [];
  }

  final j1 = json.decode(v);
  return videoMediasFromJSON(j1);
}

List<Media> videoMediasFromJSON(dynamic json) {
  List<Media> m = [];
  if (json is List) {
    m = json.map((e) => videoMediaFromJSON(e)).whereNotNull().toList();
  } else {
    if (videoMediaFromJSON(json) != null) {
      m.add(videoMediaFromJSON(json)!);
    }
  }
  return m;
}

Media? videoMediaFromJSON(dynamic json) {
  if (json["resource"] != null) {
    var extras = json["extras"] != null
        ? (json["extras"] as Map)
            .map((key, value) => MapEntry(key.toString(), value.toString()))
        : null;
    var httpHeaders = json["http_headers"] != null
        ? (json["http_headers"] as Map)
            .map((key, value) => MapEntry(key.toString(), value.toString()))
        : null;
    return Media(
      json["resource"],
      extras: extras,
      httpHeaders: httpHeaders,
    );
  }
  return null;
}

Map<String, dynamic>? parseSubtitleConfiguration(
    ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return subtitleConfigurationFromJSON(theme, j1);
}

Map<String, dynamic> subtitleConfigurationFromJSON(
    ThemeData theme, dynamic json) {
  SubtitleViewConfiguration configuration = SubtitleViewConfiguration(
    style: json["text_style"] != null
        ? textStyleFromJson(theme, json["text_style"])!
        : const TextStyle(
            height: 1.4,
            fontSize: 32.0,
            letterSpacing: 0.0,
            wordSpacing: 0.0,
            color: Color(0xffffffff),
            fontWeight: FontWeight.normal,
            backgroundColor: Color(0xaa000000)),
    visible: parseBool(json["visible"], true)!,
    textScaleFactor: parseDouble(json["text_scale_factor"]),
    textAlign: parseTextAlign(json["text_align"], TextAlign.center)!,
    padding: edgeInsetsFromJson(json["padding"]) ??
        const EdgeInsets.fromLTRB(16.0, 0.0, 16.0, 24.0),
  );

  return <String, dynamic>{
    "src": json["src"],
    "title": json["title"],
    "language": json["language"],
    "subtitleViewConfiguration": configuration
  };
}

SubtitleTrack parseSubtitleTrack(
    AssetSrc assetSrc, String? title, String? language) {
  if (assetSrc.isFile) {
    String filePath = assetSrc.path;
    File file = File(filePath);
    String content = file.readAsStringSync();
    return SubtitleTrack.data(content, title: title, language: language);
  } else {
    return SubtitleTrack.uri(assetSrc.path, title: title, language: language);
  }
}

VideoControllerConfiguration? parseControllerConfiguration(
    Control control, String propName,
    [VideoControllerConfiguration? defValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return controllerConfigurationFromJSON(j1);
}

VideoControllerConfiguration? controllerConfigurationFromJSON(dynamic json) {
  return VideoControllerConfiguration(
    vo: json["output_driver"],
    hwdec: json["hardware_decoding_api"],
    enableHardwareAcceleration:
        parseBool(json["enable_hardware_acceleration"], true)!,
  );
}
