import 'package:geolocator/geolocator.dart';

LocationAccuracy parseLocationAccuracy(String accuracy) {
  LocationAccuracy locationAccuracy;
  switch (accuracy) {
    case "best":
      locationAccuracy = LocationAccuracy.best;
    case "bestForNavigation":
      locationAccuracy = LocationAccuracy.bestForNavigation;
    case "high":
      locationAccuracy = LocationAccuracy.high;
    case "medium":
      locationAccuracy = LocationAccuracy.medium;
    case "low":
      locationAccuracy = LocationAccuracy.low;
    case "lowest":
      locationAccuracy = LocationAccuracy.lowest;
    case "reduced":
      locationAccuracy = LocationAccuracy.reduced;
    default:
      locationAccuracy = LocationAccuracy.best;
  }
  return locationAccuracy;
}
