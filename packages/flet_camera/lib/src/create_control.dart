import 'package:flet/flet.dart';

import 'camera.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "camera":
      return CameraControl(
        key: args.key,
        parent: args.parent,
        control: args.control,
        children: args.children,
        parentDisabled: args.parentDisabled,
        backend: args.backend,
      );
    default:
      return null;
  }
};

Future<void> ensureInitialized() async {
  // nothing to initialize
}
