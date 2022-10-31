import 'package:flutter/material.dart';

import '../../flet.dart';
import '../models/control.dart';
import 'create_control.dart';

class FletAppControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const FletAppControl({Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("FletApp build: ${control.id}");

    var url = control.attrString("url", "")!;

    return constrainedControl(
        context,
        FletApp(
          pageUrl: url,
        ),
        parent,
        control);
  }
}
