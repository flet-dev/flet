import 'package:flutter/material.dart';
import 'package:screenshot/screenshot.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/time.dart';
import 'base_controls.dart';

class ScreenshotControl extends StatefulWidget {
  final Control control;

  ScreenshotControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<ScreenshotControl> createState() => _InteractiveViewerControlState();
}

class _InteractiveViewerControlState extends State<ScreenshotControl> {
  final ScreenshotController _screenshotController = ScreenshotController();

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Screenshot.$name($args)");
    switch (name) {
      case "capture":
        return await _screenshotController.capture(
            pixelRatio: args["pixel_ratio"],
            delay: parseDuration(
                args["delay"], const Duration(milliseconds: 20))!);
      default:
        throw Exception("Unknown Screenshot method: $name");
    }
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Screenshot build: ${widget.control.id}");

    var screenshot = Screenshot(
        controller: _screenshotController,
        child: widget.control.buildWidget("content"));

    return BaseControl(control: widget.control, child: screenshot);
  }
}
