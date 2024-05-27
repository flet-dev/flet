import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:screenshot/screenshot.dart';

import '../controls/create_control.dart';
import '../models/control.dart';

Future<String?> takeScreenshot(String id, Control? control) async {
  debugPrint("Taking Screenshot of: $id");
  ScreenshotController screenshotController = ScreenshotController();
  Uint8List? capturedImage;

  capturedImage = await screenshotController.captureFromWidget(
      createControl(control, id, control?.isDisabled ?? false));
  debugPrint("Captured image: ${capturedImage.length}");
  return base64Encode(capturedImage);
}
