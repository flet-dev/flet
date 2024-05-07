import 'dart:convert';

import 'package:geolocator/geolocator.dart';

LocationAccuracy? parseLocationAccuracy(String? accuracy,
    [LocationAccuracy? defaultValue]) {
  switch (accuracy?.toLowerCase()) {
    case "best":
      return LocationAccuracy.best;
    case "bestfornavigation":
      return LocationAccuracy.bestForNavigation;
    case "high":
      return LocationAccuracy.high;
    case "medium":
      return LocationAccuracy.medium;
    case "low":
      return LocationAccuracy.low;
    case "lowest":
      return LocationAccuracy.lowest;
    case "reduced":
      return LocationAccuracy.reduced;
    default:
      return defaultValue;
  }
}

String? positionToJson(Position? position) {
  if (position == null) {
    return null;
  }
  String positionAsJson = json.encode({
    "latitude": position.latitude,
    "longitude": position.longitude,
    "accuracy": position.accuracy,
    "altitude": position.altitude,
    "speed": position.speed,
    "speed_accuracy": position.speedAccuracy,
    "heading": position.heading,
    "heading_accuracy": position.headingAccuracy,
    "timestamp": position.timestamp.toIso8601String(),
    "floor": position.floor,
    "is_mocked": position.isMocked,
  });
  return positionAsJson;
}
