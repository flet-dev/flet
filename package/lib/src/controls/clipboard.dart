import 'package:flet/src/flet_server.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

import '../flet_app_services.dart';
import '../models/control.dart';

class ClipboardControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final Widget? nextChild;

  const ClipboardControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.nextChild});

  @override
  State<ClipboardControl> createState() => _ClipboardControlState();
}

class _ClipboardControlState extends State<ClipboardControl> {
  FletServer? _server;

  @override
  void deactivate() {
    _server?.controlInvokeMethods.remove(widget.control.id);
    super.deactivate();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Clipboard build: ${widget.control.id}");

    _server = FletAppServices.of(context).server;
    _server?.controlInvokeMethods[widget.control.id] =
        (methodName, args) async {
      switch (methodName) {
        case "set_data":
          await Clipboard.setData(ClipboardData(text: args["data"]!));
          return null;
        case "get_data":
          return (await Clipboard.getData(Clipboard.kTextPlain))?.text;
      }
      return null;
    };

    return widget.nextChild ?? const SizedBox.shrink();
  }
}
