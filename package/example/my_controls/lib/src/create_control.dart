import 'package:flet/flet.dart';

import 'my_control.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "my_org:my_control":
      return MyControl(
        control: args.control,
        children: args.children,
        parentDisabled: args.parentDisabled,
        parentAdaptive: args.parentAdaptive,
      );
    default:
      return null;
  }
};
