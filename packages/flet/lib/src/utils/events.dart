import 'package:flutter/gestures.dart';

extension ScaleEndDetailsExtension on ScaleEndDetails {
  Map<String, dynamic> toMap() => {
        "pc": pointerCount,
        "v": {
          "x": velocity.pixelsPerSecond.dx,
          "y": velocity.pixelsPerSecond.dy
        },
      };
}

extension ScaleUpdateDetailsExtension on ScaleUpdateDetails {
  Map<String, dynamic> toMap() => {
        "gfp": {"x": focalPoint.dx, "y": focalPoint.dy},
        "fpd": {"x": focalPointDelta.dx, "y": focalPointDelta.dy},
        "lfp": {"x": localFocalPoint.dx, "y": localFocalPoint.dy},
        "pc": pointerCount,
        "hs": horizontalScale,
        "vs": verticalScale,
        "s": scale,
        "rot": rotation,
        "ts": sourceTimeStamp,
      };
}

extension ScaleStartDetailsExtension on ScaleStartDetails {
  Map<String, dynamic> toMap() => {
        "gfp": {"x": focalPoint.dx, "y": focalPoint.dy},
        "lfp": {"x": localFocalPoint.dx, "y": localFocalPoint.dy},
        "pc": pointerCount,
        "ts": sourceTimeStamp,
      };
}

extension DragEndDetailsExtension on DragEndDetails {
  Map<String, dynamic> toMap() => {
        "l": {"x": localPosition.dx, "y": localPosition.dy},
        "g": {"x": globalPosition.dx, "y": globalPosition.dy},
        "v": {
          "x": velocity.pixelsPerSecond.dx,
          "y": velocity.pixelsPerSecond.dy
        },
        "pv": primaryVelocity,
      };
}

extension LongPressEndDetailsExtension on LongPressEndDetails {
  Map<String, dynamic> toMap() => {
        "l": {"x": localPosition.dx, "y": localPosition.dy},
        "g": {"x": globalPosition.dx, "y": globalPosition.dy},
        "v": {
          "x": velocity.pixelsPerSecond.dx,
          "y": velocity.pixelsPerSecond.dy
        },
      };
}

extension LongPressStartDetailsExtension on LongPressStartDetails {
  Map<String, dynamic> toMap() => {
        "l": {"x": localPosition.dx, "y": localPosition.dy},
        "g": {"x": globalPosition.dx, "y": globalPosition.dy},
      };
}

extension TapDownDetailsExtension on TapDownDetails {
  Map<String, dynamic> toMap() => {
        "k": kind?.name,
        "l": {"x": localPosition.dx, "y": localPosition.dy},
        "g": {"x": globalPosition.dx, "y": globalPosition.dy},
      };
}

extension TapUpDetailsExtension on TapUpDetails {
  Map<String, dynamic> toMap() => {
        "k": kind.name,
        "l": {"x": localPosition.dx, "y": localPosition.dy},
        "g": {"x": globalPosition.dx, "y": globalPosition.dy},
      };
}

extension DragStartDetailsExtension on DragStartDetails {
  Map<String, dynamic> toMap() => {
        "k": kind?.name,
        "l": {"x": localPosition.dx, "y": localPosition.dy},
        "g": {"x": globalPosition.dx, "y": globalPosition.dy},
        "ts": sourceTimeStamp,
      };
}

extension DragUpdateDetailsExtension on DragUpdateDetails {
  Map<String, dynamic> toMap(
      [Offset? previousLocalPosition, Offset? previousGlobalPosition]) {
    final localDelta = previousLocalPosition != null
        ? localPosition - previousLocalPosition
        : null;
    final globalDelta = previousGlobalPosition != null
        ? globalPosition - previousGlobalPosition
        : null;
    return {
      "l": {"x": localPosition.dx, "y": localPosition.dy},
      "g": {"x": globalPosition.dx, "y": globalPosition.dy},
      "ld": {"x": localDelta?.dx, "y": localDelta?.dy},
      "gd": {"x": globalDelta?.dx, "y": globalDelta?.dy},
      "pd": primaryDelta,
      "ts": sourceTimeStamp,
    };
  }
}

extension PointerEventExtension on PointerEvent {
  Map<String, dynamic> toMap([Offset? previousLocalPosition]) {
    var localDelta = previousLocalPosition != null
        ? localPosition - previousLocalPosition
        : null;
    return {
      "k": kind.name,
      "l": {"x": localPosition.dx, "y": localPosition.dy},
      "g": {"x": position.dx, "y": position.dy},
      "ts": timeStamp,
      "dev": device,
      "ps": pressure,
      "pMin": pressureMin,
      "pMax": pressureMax,
      "dist": distance,
      "distMax": distanceMax,
      "size": size,
      "rMj": radiusMajor,
      "rMn": radiusMinor,
      "rMin": radiusMin,
      "rMax": radiusMax,
      "or": orientation,
      "tilt": tilt,
      "ld": {"x": localDelta?.dx, "y": localDelta?.dy},
    };
  }
}

extension PointerScrollEventExtension on PointerScrollEvent {
  Map<String, dynamic> toMap() => {
        "l": {"x": localPosition.dx, "y": localPosition.dy},
        "g": {"x": position.dx, "y": position.dy},
        "sd": {"x": scrollDelta.dx, "y": scrollDelta.dy},
      };
}
