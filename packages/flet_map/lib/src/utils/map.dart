import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

MapOptions parseMapOptions(
    Control control, String propName, BuildContext context) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return const MapOptions();
  }
  ThemeData theme = Theme.of(context);

  final j1 = json.decode(v);
  return mapOptionsFromJSON(j1, theme);
}

MapOptions mapOptionsFromJSON(dynamic json, ThemeData theme) {
  return MapOptions(
    applyPointerTranslucencyToLayers:
        parseBoolFromJson(json["apply_pointer_translucency_to_layers"], true)!,
    backgroundColor:
        parseColorFromJson(theme, json["bgcolor"]) ?? const Color(0xFFE0E0E0),
    // cameraConstraint: ,
    // crs: ,
    // initialCameraFit: ,
    initialCenter: json["initial_center"] != null
        ? LatLng(parseDoubleFromJson(json["initial_center"][0], 50.5)!,
            parseDoubleFromJson(json["initial_center"][1], 30.51)!)
        : const LatLng(50.5, 30.51),
    initialRotation: parseDoubleFromJson(json["initial_rotation"], 0.0)!,
    initialZoom: parseDoubleFromJson(json["initial_zoom"], 13.0)!,
    // interactionOptions: ,
    keepAlive: parseBoolFromJson(json["keep_alive"], false)!,
    maxZoom: parseDoubleFromJson(json["max_zoom"]),
    minZoom: parseDoubleFromJson(json["min_zoom"]),
  );
}

TileLayer? tileLayerFromJSON(dynamic json) {
  // `wmsOptions` or `urlTemplate` must be provided to generate a tile URL
  // For now, only `urlTemplate` is supported
  if (json["url_template"] == null) {
    return null;
  }
  return TileLayer(
    urlTemplate: json["url_template"],
    fallbackUrl: json["fallback_url"],
    tileSize: parseDoubleFromJson(json["tile_size"], 256)!,
    minNativeZoom: parseIntFromJson(json["min_native_zoom"], 0)!,
    maxNativeZoom: parseIntFromJson(json["max_native_zoom"], 19)!,
    zoomReverse: parseBoolFromJson(json["zoom_reverse"], false)!,
    zoomOffset: parseDoubleFromJson(json["zoom_offset"], 0.0)!,
    // additionalOptions: ,
    // subdomains: ,
    keepBuffer: parseIntFromJson(json["keep_buffer"], 2)!,
    panBuffer: parseIntFromJson(json["pan_buffer"], 1)!,
    tms: parseBoolFromJson(json["tms"], false)!,
    maxZoom: parseDoubleFromJson(json["max_zoom"], double.infinity)!,
    minZoom: parseDoubleFromJson(json["min_zoom"], 0)!,
  );
}

List<Widget> parseMapChildren(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return [];
  }

  final j1 = json.decode(v);
  return mapChildrenFromJSON(j1);
}

List<Widget> mapChildrenFromJSON(dynamic json) {
  List<Widget> m = [];
  if (json is List) {
    m = json.map((e) => tileLayerFromJSON(e)).whereNotNull().toList();
  }
  return m;
}

LatLng? parseLatLng(Control control, String propName, [LatLng? defValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return latLngFromJson(j1);
}

LatLng latLngFromJson(Map<String, dynamic> json) {
  return LatLng(parseDouble(json['latitude']), parseDouble(json['longitude']));
}
