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

ImageFormatGroup? parseImageFormatGroup(dynamic value,
    [ImageFormatGroup? defaultValue]) {
  return parseEnum(ImageFormatGroup.values, value, defaultValue);
}

FlashMode? parseFlashMode(dynamic value, [FlashMode? defaultValue]) {
  return parseEnum(FlashMode.values, value, defaultValue);
}

ExposureMode? parseExposureMode(dynamic value, [ExposureMode? defaultValue]) {
  return parseEnum(ExposureMode.values, value, defaultValue);
}

FocusMode? parseFocusMode(dynamic value, [FocusMode? defaultValue]) {
  return parseEnum(FocusMode.values, value, defaultValue);
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
    case ImageFormatGroup.nv21:
    case ImageFormatGroup.yuv420:
      return encodeCameraImagePayload(cameraImageToPayload(image));
    case ImageFormatGroup.jpeg:
      if (image.planes.isEmpty) {
        return Uint8List(0);
      }
      return image.planes.first.bytes;
    default:
      return Uint8List(0);
  }
}

Map<String, dynamic> cameraImageToPayload(CameraImage image) {
  return {
    "width": image.width,
    "height": image.height,
    "format": image.format.group.name,
    "planes": image.planes
        .map(
          (p) => {
            "bytes": Uint8List.fromList(p.bytes),
            "bytes_per_row": p.bytesPerRow,
            "bytes_per_pixel": p.bytesPerPixel,
          },
        )
        .toList(),
  };
}

Uint8List encodeCameraImagePayload(Map<String, dynamic> payload) {
  final format = payload["format"];
  switch (format) {
    case "bgra8888":
      return _encodeBgra8888Payload(payload);
    case "nv21":
      return _encodeNv21Payload(payload);
    case "yuv420":
      return _encodeYuv420Payload(payload);
    case "jpeg":
      final planes = payload["planes"];
      if (planes is List && planes.isNotEmpty) {
        final first = planes.first;
        if (first is Map && first["bytes"] is Uint8List) {
          return first["bytes"] as Uint8List;
        }
      }
      return Uint8List(0);
    default:
      return Uint8List(0);
  }
}

Uint8List _encodeBgra8888Payload(Map<String, dynamic> payload) {
  final width = payload["width"];
  final height = payload["height"];
  final planes = payload["planes"];
  if (width is! int || height is! int || planes is! List || planes.isEmpty) {
    return Uint8List(0);
  }
  final plane = planes.first;
  if (plane is! Map || plane["bytes"] is! Uint8List) {
    return Uint8List(0);
  }
  final bytes = plane["bytes"] as Uint8List;
  final bytesPerRow = plane["bytes_per_row"];
  if (bytesPerRow is! int) {
    return Uint8List(0);
  }
  final img.Image converted = img.Image.fromBytes(
    width: width,
    height: height,
    bytes: bytes.buffer,
    numChannels: 4,
    rowStride: bytesPerRow,
    order: img.ChannelOrder.bgra,
  );
  return Uint8List.fromList(img.encodeJpg(converted));
}

Uint8List _encodeYuv420Payload(Map<String, dynamic> payload) {
  final width = payload["width"];
  final height = payload["height"];
  final planes = payload["planes"];
  if (width is! int || height is! int || planes is! List || planes.isEmpty) {
    return Uint8List(0);
  }
  final yPlane = planes[0];
  final uPlane = planes.length > 1 ? planes[1] : null;
  final vPlane = planes.length > 2 ? planes[2] : null;
  if (yPlane is! Map || yPlane["bytes"] is! Uint8List) {
    return Uint8List(0);
  }
  final yBytes = yPlane["bytes"] as Uint8List;
  final yBytesPerRow = yPlane["bytes_per_row"];
  if (yBytesPerRow is! int) {
    return Uint8List(0);
  }
  final uBytes = uPlane is Map && uPlane["bytes"] is Uint8List
      ? uPlane["bytes"] as Uint8List
      : null;
  final vBytes = vPlane is Map && vPlane["bytes"] is Uint8List
      ? vPlane["bytes"] as Uint8List
      : null;
  final uvPixelStride = uPlane is Map && uPlane["bytes_per_pixel"] is int
      ? uPlane["bytes_per_pixel"] as int
      : 1;
  final uvRowStride = uPlane is Map && uPlane["bytes_per_row"] is int
      ? uPlane["bytes_per_row"] as int
      : 0;

  final img.Image converted = img.Image(width: width, height: height);
  for (int y = 0; y < height; y++) {
    final int yRow = y * yBytesPerRow;
    final int uvRow = uvRowStride * (y >> 1);
    for (int x = 0; x < width; x++) {
      final int yIndex = yRow + x;
      if (yIndex >= yBytes.length) {
        continue;
      }
      final int uvIndex = uvRow + (x >> 1) * uvPixelStride;
      final int yp = yBytes[yIndex];
      final int up =
          (uBytes != null && uvIndex < uBytes.length) ? uBytes[uvIndex] : 128;
      final int vp =
          (vBytes != null && uvIndex < vBytes.length) ? vBytes[uvIndex] : 128;
      final (int r, int g, int b) = _yuvToRgb(yp, up, vp);
      converted.setPixelRgba(x, y, r, g, b, 255);
    }
  }
  return Uint8List.fromList(img.encodeJpg(converted));
}

Uint8List _encodeNv21Payload(Map<String, dynamic> payload) {
  final width = payload["width"];
  final height = payload["height"];
  final planes = payload["planes"];
  if (width is! int || height is! int || planes is! List || planes.length < 2) {
    return Uint8List(0);
  }
  final yPlane = planes[0];
  final uvPlane = planes[1];
  if (yPlane is! Map ||
      uvPlane is! Map ||
      yPlane["bytes"] is! Uint8List ||
      uvPlane["bytes"] is! Uint8List) {
    return Uint8List(0);
  }
  final yBytes = yPlane["bytes"] as Uint8List;
  final uvBytes = uvPlane["bytes"] as Uint8List;
  final yBytesPerRow = yPlane["bytes_per_row"];
  final uvRowStride = uvPlane["bytes_per_row"];
  if (yBytesPerRow is! int || uvRowStride is! int) {
    return Uint8List(0);
  }
  final uvPixelStride =
      uvPlane["bytes_per_pixel"] is int ? uvPlane["bytes_per_pixel"] as int : 2;
  final img.Image converted = img.Image(width: width, height: height);
  for (int y = 0; y < height; y++) {
    final int yRow = y * yBytesPerRow;
    final int uvRow = uvRowStride * (y >> 1);
    for (int x = 0; x < width; x++) {
      final int yIndex = yRow + x;
      if (yIndex >= yBytes.length) {
        continue;
      }
      final int uvIndex = uvRow + (x >> 1) * uvPixelStride;
      if (uvIndex + 1 >= uvBytes.length) {
        continue;
      }
      final int yp = yBytes[yIndex];
      final int vp = uvBytes[uvIndex];
      final int up = uvBytes[uvIndex + 1];
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
