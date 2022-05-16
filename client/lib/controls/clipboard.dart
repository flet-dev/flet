import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

import '../models/control.dart';

class ClipboardControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const ClipboardControl({Key? key, this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Clipboard build: ${control.id}");

    var value = control.attrString("value");

    if (value != null) {
      debugPrint("Clipboard JSON value: $value");

      var jv = json.decode(value);
      var text = jv["d"] as String?;
      if (text != null) {
        Clipboard.setData(ClipboardData(text: text));
      }
    }

    return const SizedBox.shrink();
  }
}
