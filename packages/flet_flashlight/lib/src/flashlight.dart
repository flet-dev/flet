import 'dart:io' show Platform;
import 'dart:io';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:torch_light/torch_light.dart';

class FlashlightControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final Widget? nextChild;
  final FletControlBackend backend;

  const FlashlightControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.nextChild,
      required this.backend});

  @override
  State<FlashlightControl> createState() => _FlashlightControlState();
}

class _FlashlightControlState extends State<FlashlightControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("FlashLightControl build: ${widget.control.id}");

    if (Platform.isIOS || Platform.isAndroid) {
      () async {
        widget.backend.subscribeMethods(widget.control.id,
            (meathodName, args) async {
          switch (meathodName) {
            case "on":
              try {
                await TorchLight.enableTorch();
                return "1";
              } on Exception catch (_) {
                debugPrint("Couldn't enable Flash: $_");
                return "0";
              }
            case "off":
              try {
                await TorchLight.disableTorch();
                return "1";
              } on Exception catch (_) {
                debugPrint("Couldn't disable Flash");
                return "0";
              }
          }
          return null;
        });
      }();

      return const SizedBox.shrink();
    } else {
      return const ErrorControl(
          "FlashLight control is not supported on this platform yet.");
    }
  }
}
