import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';

class ClipboardControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final Widget? nextChild;
  final FletControlBackend backend;

  const ClipboardControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.nextChild,
      required this.backend});

  @override
  State<ClipboardControl> createState() => _ClipboardControlState();
}

class _ClipboardControlState extends State<ClipboardControl> {
  @override
  void deactivate() {
    widget.backend.unsubscribeMethods(widget.control.id);
    super.deactivate();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Clipboard build: ${widget.control.id}");

    widget.backend.subscribeMethods(widget.control.id,
        (methodName, args) async {
      switch (methodName) {
        case "set_data":
          await Clipboard.setData(ClipboardData(text: args["data"]!));
          return null;
        case "get_data":
          return (await Clipboard.getData(Clipboard.kTextPlain))?.text;
      }
      return null;
    });

    return widget.nextChild ?? const SizedBox.shrink();
  }
}
