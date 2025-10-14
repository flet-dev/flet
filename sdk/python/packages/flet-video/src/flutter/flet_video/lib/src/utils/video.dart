import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';

import "file_utils_web.dart" if (dart.library.io) 'file_utils_io.dart';

Media? parseVideoMedia(dynamic value, [Media? defaultValue]) {
  if (value == null || value["resource"] == null) return defaultValue;

  final extras = (value["extras"] as Map?)?.map(
    (key, val) => MapEntry(key.toString(), val.toString()),
  );

  final httpHeaders = (value["http_headers"] as Map?)?.map(
    (key, val) => MapEntry(key.toString(), val.toString()),
  );

  return Media(value["resource"], extras: extras, httpHeaders: httpHeaders);
}

List<Media>? parseVideoMedias(dynamic value, [List<Media>? defaultValue]) {
  if (value == null) return defaultValue;

  if (value is List) {
    return value.map((e) => parseVideoMedia(e)).nonNulls.toList();
  }

  final media = parseVideoMedia(value);
  return media != null ? [media] : defaultValue;
}

SubtitleViewConfiguration? parseSubtitleConfiguration(
    dynamic value, ThemeData theme,
    [SubtitleViewConfiguration? defaultValue]) {
  if (value == null) return defaultValue;

  return SubtitleViewConfiguration(
    style: parseTextStyle(
        value["text_style"],
        theme,
        const TextStyle(
            height: 1.4,
            fontSize: 32.0,
            letterSpacing: 0.0,
            wordSpacing: 0.0,
            color: Color(0xffffffff),
            fontWeight: FontWeight.normal,
            backgroundColor: Color(0xaa000000)))!,
    visible: parseBool(value["visible"], true)!,
    textScaler: TextScaler.linear(parseDouble(value["text_scale_factor"], 1)!),
    textAlign: parseTextAlign(value["text_align"], TextAlign.center)!,
    padding: parsePadding(
        value["padding"], const EdgeInsets.fromLTRB(16.0, 0.0, 16.0, 24.0))!,
  );
}

bool isUrl(String value) {
  final urlPattern = RegExp(r'^(http:\/\/|https:\/\/|www\.)');
  return urlPattern.hasMatch(value);
}

SubtitleTrack? parseSubtitleTrack(
  dynamic value,
  BuildContext context, [
  SubtitleTrack? defaultValue,
]) {
  if (value == null) return defaultValue;

  String src;
  final String rawSrc = value["src"] as String;
  if (rawSrc == "none") return SubtitleTrack.no();
  if (rawSrc == "auto") return SubtitleTrack.auto();

  bool uri = false;

  if (isUrl(rawSrc)) {
    uri = true;
    src = rawSrc;
  } else {
    // Non-URL: on non-web platforms, try reading it as a file path
    String? fileContents;
    if (!isWebPlatform()) {
      // todo: add support for relative paths to assets-dir
      fileContents = readFileAsStringIfExists(rawSrc);
    }

    // If reading succeeded, use the file’s contents;
    // otherwise assume rawSrc is already subtitle text
    src = fileContents ?? rawSrc;
    uri = false;
  }

  return SubtitleTrack(
    src,
    value["title"],
    value["language"],
    channelscount: parseInt(value["channels_count"]),
    channels: value["channels"],
    samplerate: parseInt(value["sample_rate"]),
    fps: parseDouble(value["fps"]),
    bitrate: parseInt(value["bitrate"]),
    rotate: parseInt(value["rotate"]),
    par: parseDouble(value["par"]),
    audiochannels: parseInt(value["audio_channels"]),
    albumart: parseBool(value["album_art"]),
    codec: value["codec"],
    decoder: value["decoder"],
    data: !uri,
    // true when providing raw subtitle text
    uri: uri, // true when providing a URL
  );
}

VideoControllerConfiguration? parseControllerConfiguration(dynamic value,
    [VideoControllerConfiguration? defaultValue]) {
  if (value == null) return defaultValue;
  return VideoControllerConfiguration(
    vo: value["output_driver"],
    hwdec: value["hardware_decoding_api"],
    enableHardwareAcceleration:
        parseBool(value["enable_hardware_acceleration"], true)!,
    width: value["width"],
    height: value["height"],
    scale: parseDouble(value["scale"], 1.0)!,
  );
}

PlaylistMode? parsePlaylistMode(String? value, [PlaylistMode? defaultValue]) {
  if (value == null) return defaultValue;
  return PlaylistMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}
