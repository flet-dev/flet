import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:media_kit/media_kit.dart';

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
    json.map((e) => videoMediaFromJSON(e)).toList().forEach((e) {
      if (e != null) {
        m.add(e);
      }
    });
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
