import 'package:flet/flet.dart';

import 'geolocator.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "geolocator":
      return GeolocatorControl(
          parent: args.parent, control: args.control, backend: args.backend);
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to do
}
