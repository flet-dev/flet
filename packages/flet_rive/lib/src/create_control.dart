import 'package:flet/flet.dart';

import 'rive.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "rive":
      return RiveControl(
          parent: args.parent,
          control: args.control,
          children: args.children,
          parentDisabled: args.parentDisabled,
          parentAdaptive: args.parentAdaptive,
          backend: args.backend);
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to initialize
}
