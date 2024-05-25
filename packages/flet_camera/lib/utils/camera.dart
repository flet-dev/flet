import 'package:camera/camera.dart';
import 'package:collection/collection.dart';

ResolutionPreset? parseResolutionPreset(String? resolutionPreset,
    [ResolutionPreset? defaultValue]) {
  if (resolutionPreset == null) {
    return defaultValue;
  }
  return ResolutionPreset.values.firstWhereOrNull((e) =>
          e.toString().toLowerCase() == resolutionPreset.toLowerCase()) ??
      defaultValue;
}

ImageFormatGroup? parseImageFormatGroup(String? imageFormatGroup,
    [ImageFormatGroup? defaultValue]) {
  if (imageFormatGroup == null) {
    return defaultValue;
  }
  return ImageFormatGroup.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == imageFormatGroup.toLowerCase()) ??
      defaultValue;
}

ExposureMode? parseExposureMode(String? resolutionPreset,
    [ExposureMode? defaultValue]) {
  if (resolutionPreset == null) {
    return defaultValue;
  }
  return ExposureMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == resolutionPreset.toLowerCase()) ??
      defaultValue;
}
