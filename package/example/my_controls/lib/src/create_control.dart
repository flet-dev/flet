import 'package:flet/flet.dart';

import 'my_control.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.typeName) {
    case "my_org:my_control":
      return MyControl(
          control: args.control,
          children: args.children,
          parentDisabled: args.parentDisabled);
    default:
      return null;
  }
};
