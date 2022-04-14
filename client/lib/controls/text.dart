import 'package:flet_view/controls/create_control.dart';
import 'package:flutter/widgets.dart';

import '../models/control.dart';

class TextControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const TextControl({Key? key, this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Text build: ${control.id}");
    return commonControl(
        Text(control.attrString("value", "")!), parent, control);
  }
}
