import 'package:flet/flet.dart';

import 'geolocator.dart';

class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "Geolocator":
        return GeolocatorService(control: control);
      default:
        return null;
    }
  }
}
