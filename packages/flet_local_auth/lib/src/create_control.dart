import "package:flet/flet.dart";

import "local_auth.dart";

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "localauthentication":
      return LocalAuthenticationControl(
          parent: args.parent, control: args.control, backend: args.backend);
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to initialize
}
