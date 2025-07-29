import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/cupertino.dart';
import 'package:flutter/rendering.dart';

import '../flet_service.dart';
import '../utils/keys.dart';

class ScreenshotService extends FletService {
  ScreenshotService({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("ScreenshotService(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void update() {
    debugPrint(
        "ScreenshotService(${control.id}).update: ${control.properties}");
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("ScreenshotService.$name($args)");
    switch (name) {
      case "capture":
        await Future.delayed(args["delay"] ?? const Duration(milliseconds: 10));
        var screenshotKey = parseKey(args["screenshot_key"]);
        var globalKey = screenshotKey != null
            ? control.backend.globalKeys[screenshotKey.toString()]
            : null;
        if (globalKey == null) {
          throw Exception(
              "Control with provided screenshot_key not found: $screenshotKey");
        }
        var pixelRatio = args["pixel_ratio"] ??
            (globalKey.currentContext != null
                ? MediaQuery.devicePixelRatioOf(globalKey.currentContext!)
                : 1.0);
        try {
          RenderRepaintBoundary? boundary = globalKey.currentContext
              ?.findRenderObject() as RenderRepaintBoundary?;
          if (boundary != null) {
            var image = await boundary.toImage(pixelRatio: pixelRatio);
            ByteData? byteData =
                await image.toByteData(format: ui.ImageByteFormat.png);
            image.dispose();
            return byteData?.buffer.asUint8List();
          }
        } catch (e) {
          throw Exception("Error capturing widget: $e");
        }
      default:
        throw Exception("Unknown Screenshot method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("ScreenshotService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
