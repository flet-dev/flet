import 'package:flet/flet.dart';

import 'permission_handler.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "permission_handler":
      return PermissionHandlerControl(
          parent: args.parent, control: args.control, backend: args.backend);
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to do
}
