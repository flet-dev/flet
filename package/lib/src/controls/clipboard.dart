import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

import '../models/control.dart';

class ClipboardControl extends StatefulWidget {
  final Control? parent;
  final Control control;

  const ClipboardControl(
      {Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  State<ClipboardControl> createState() => _ClipboardControlState();
}

class _ClipboardControlState extends State<ClipboardControl> {
  String _ts = "";

  @override
  Widget build(BuildContext context) {
    debugPrint("Clipboard build: ${widget.control.id}");

    var value = widget.control.attrString("value");

    if (value != null) {
      debugPrint("Clipboard JSON value: $value");

      var jv = json.decode(value);
      var ts = jv["ts"] as String;
      var text = jv["d"] as String?;
      if (text != null && ts != _ts) {
        Clipboard.setData(ClipboardData(text: text));
        _ts = ts;
      }
    }

    return const SizedBox.shrink();
  }
}
