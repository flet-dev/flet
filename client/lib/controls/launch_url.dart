import 'dart:convert';

import 'package:flutter/widgets.dart';
import 'package:url_launcher/url_launcher.dart';

import '../models/control.dart';

class LaunchUrlControl extends StatefulWidget {
  final Control? parent;
  final Control control;

  const LaunchUrlControl(
      {Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  State<LaunchUrlControl> createState() => _LaunchUrlControlState();
}

class _LaunchUrlControlState extends State<LaunchUrlControl> {
  String _ts = "";

  @override
  Widget build(BuildContext context) {
    debugPrint("Launch URL build: ${widget.control.id}");

    var value = widget.control.attrString("value");

    if (value != null) {
      debugPrint("Launch URL JSON value: $value");

      var jv = json.decode(value);
      var ts = jv["ts"] as String;
      var url = jv["url"] as String?;
      if (url != null && ts != _ts) {
        launchUrl(Uri.parse(url));
        _ts = ts;
      }
    }

    return const SizedBox.shrink();
  }
}
