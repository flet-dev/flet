import 'package:flet/flet.dart';

import 'audio.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "audio":
      return AudioControl(
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
