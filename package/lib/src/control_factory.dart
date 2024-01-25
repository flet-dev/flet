import 'package:flutter/widgets.dart';

import 'models/control.dart';

class CreateControlArgs {
  final Key? key;
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  CreateControlArgs(
      this.key, this.parent, this.control, this.children, this.parentDisabled);
}

typedef CreateControlFactory = Widget? Function(CreateControlArgs args);
