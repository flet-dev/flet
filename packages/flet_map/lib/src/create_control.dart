import 'package:flet/flet.dart';

import 'map.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "map":
      return MapControl(
          parent: args.parent,
          control: args.control,
          nextChild: args.nextChild,
          backend: args.backend);
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to initialize
}
