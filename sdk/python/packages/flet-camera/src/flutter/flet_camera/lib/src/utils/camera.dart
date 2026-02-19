import 'dart:math';

import 'package:camera/camera.dart';
import 'package:flet/flet.dart';
import 'package:flutter/services.dart';
import 'package:image/image.dart' as img;

CameraDescription? parseCameraDescription(dynamic value) {
  if (value == null) return null;
  if (value is CameraDescription) return value;
  if (value is Map) {
    final lensDirection = parseEnum(CameraLensDirection.values,
        value["lens_direction"], CameraLensDirection.back)!;
    final lensType = parseEnum(
        CameraLensType.values, value["lens_type"], CameraLensType.unknown)!;
    final sensorOrientation = value["sensor_orientation"];
    final name = value["name"];
    if (name is String && sensorOrientation is int) {
      return CameraDescription(
        name: name,
        lensDirection: lensDirection,
        sensorOrientation: sensorOrientation,
        lensType: lensType,
      );
    }
  }
  return null;
}

ResolutionPreset parseResolutionPreset(dynamic value,
    [ResolutionPreset? defaultValue]) {
  return parseEnum(ResolutionPreset.values, value, defaultValue)!;
}

ImageFormatGroup? parseImageFormatGroup(dynamic value) {
  return parseEnum(ImageFormatGroup.values, value);
}

FlashMode? parseFlashMode(dynamic value) {
  return parseEnum(FlashMode.values, value);
}

ExposureMode? parseExposureMode(dynamic value) {
  return parseEnum(ExposureMode.values, value);
}

FocusMode? parseFocusMode(dynamic value) {
  return parseEnum(FocusMode.values, value);
}

DeviceOrientation? parseDeviceOrientation(dynamic value) {
  return parseEnum(DeviceOrientation.values, value);
}

Map<String, dynamic> cameraDescriptionToMap(CameraDescription description) {
  return {
    "name": description.name,
    "lens_direction": description.lensDirection.name,
    "sensor_orientation": description.sensorOrientation,
    "lens_type": description.lensType.name,
  };
}

Map<String, double>? sizeToMap(Size? size) {
  if (size == null) return null;
  return {"width": size.width, "height": size.height};
}

Map<String, dynamic> cameraValueToMap(CameraValue value) {
  return {
    "is_initialized": value.isInitialized,
    "is_recording_video": value.isRecordingVideo,
    "is_recording_paused": value.isRecordingPaused,
    "is_taking_picture": value.isTakingPicture,
    "is_streaming_images": value.isStreamingImages,
    "is_preview_paused": value.isPreviewPaused,
    "is_capture_orientation_locked": value.isCaptureOrientationLocked,
    "locked_capture_orientation": value.lockedCaptureOrientation?.name,
    "recording_orientation": value.recordingOrientation?.name,
    "device_orientation": value.deviceOrientation.name,
    "flash_mode": value.flashMode.name,
    "exposure_mode": value.exposureMode.name,
    "focus_mode": value.focusMode.name,
    "exposure_point_supported": value.exposurePointSupported,
    "focus_point_supported": value.focusPointSupported,
    "preview_pause_orientation": value.previewPauseOrientation?.name,
    "preview_size": sizeToMap(value.previewSize),
    "aspect_ratio": value.previewSize != null ? value.aspectRatio : null,
    "error_description": value.errorDescription,
    "has_error": value.hasError,
    "description": cameraDescriptionToMap(value.description),
  }..removeWhere((_, v) => v == null);
}

Map<String, dynamic> cameraImageToMap(
    CameraImage image, Uint8List encodedBytes) {
  return {
    "width": image.width,
    "height": image.height,
    "format": image.format.group.name,
    "encoded_format": "jpeg",
    "lens_aperture": image.lensAperture,
    "sensor_exposure_time": image.sensorExposureTime,
    "sensor_sensitivity": image.sensorSensitivity,
    "bytes": encodedBytes,
  }..removeWhere((_, v) => v == null);
}

Uint8List encodeCameraImage(CameraImage image) {
  switch (image.format.group) {
    case ImageFormatGroup.bgra8888:
      return _encodeBgra8888(image);
    case ImageFormatGroup.nv21:
      return _encodeNv21(image);
    case ImageFormatGroup.yuv420:
      return _encodeYuv420(image);
    case ImageFormatGroup.jpeg:
      return image.planes.first.bytes;
    default:
      return Uint8List(0);
  }
}

Uint8List _encodeBgra8888(CameraImage image) {
  final plane = image.planes.first;
  final img.Image converted = img.Image.fromBytes(
    width: image.width,
    height: image.height,
    bytes: plane.bytes.buffer,
    numChannels: 4,
    rowStride: plane.bytesPerRow,
    order: img.ChannelOrder.bgra,
  );
  return Uint8List.fromList(img.encodeJpg(converted));
}

Uint8List _encodeYuv420(CameraImage image) {
  final img.Image converted = img.Image(
    width: image.width,
    height: image.height,
  );
  final plane = image.planes[0];
  final uPlane = image.planes.length > 1 ? image.planes[1] : null;
  final vPlane = image.planes.length > 2 ? image.planes[2] : null;
  final uvPixelStride = uPlane?.bytesPerPixel ?? 1;
  final uvRowStride = uPlane?.bytesPerRow ?? 0;

  for (int y = 0; y < image.height; y++) {
    final int yRow = y * plane.bytesPerRow;
    final int uvRow = uvRowStride * (y >> 1);
    for (int x = 0; x < image.width; x++) {
      final int uvIndex = uvRow + (x >> 1) * uvPixelStride;
      final int yp = plane.bytes[yRow + x];
      final int up = uPlane?.bytes[uvIndex] ?? 128;
      final int vp = vPlane?.bytes[uvIndex] ?? 128;
      final (int r, int g, int b) = _yuvToRgb(yp, up, vp);
      converted.setPixelRgba(x, y, r, g, b, 255);
    }
  }
  return Uint8List.fromList(img.encodeJpg(converted));
}

Uint8List _encodeNv21(CameraImage image) {
  if (image.planes.length < 2) {
    return Uint8List(0);
  }
  final yPlane = image.planes[0];
  final uvPlane = image.planes[1];
  final uvPixelStride = uvPlane.bytesPerPixel ?? 2;
  final uvRowStride = uvPlane.bytesPerRow;
  final img.Image converted = img.Image(
    width: image.width,
    height: image.height,
  );

  for (int y = 0; y < image.height; y++) {
    final int yRow = y * yPlane.bytesPerRow;
    final int uvRow = uvRowStride * (y >> 1);
    for (int x = 0; x < image.width; x++) {
      final int uvIndex = uvRow + (x >> 1) * uvPixelStride;
      if (uvIndex + 1 >= uvPlane.bytes.length) {
        continue;
      }
      final int yp = yPlane.bytes[yRow + x];
      final int vp = uvPlane.bytes[uvIndex];
      final int up = uvPlane.bytes[uvIndex + 1];
      final (int r, int g, int b) = _yuvToRgb(yp, up, vp);
      converted.setPixelRgba(x, y, r, g, b, 255);
    }
  }

  return Uint8List.fromList(img.encodeJpg(converted));
}

(int, int, int) _yuvToRgb(int y, int u, int v) {
  final double yp = y.toDouble();
  final double up = u.toDouble() - 128.0;
  final double vp = v.toDouble() - 128.0;
  int r = (yp + 1.402 * vp).round();
  int g = (yp - 0.344136 * up - 0.714136 * vp).round();
  int b = (yp + 1.772 * up).round();
  r = max(0, min(255, r));
  g = max(0, min(255, g));
  b = max(0, min(255, b));
  return (r, g, b);
}
