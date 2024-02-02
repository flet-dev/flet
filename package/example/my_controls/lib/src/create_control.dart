import 'package:flet/flet.dart';

import 'my_control.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "my_org:my_control":
      return MyControl(args);
    default:
      return null;
  }
};
