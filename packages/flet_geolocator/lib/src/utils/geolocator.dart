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
