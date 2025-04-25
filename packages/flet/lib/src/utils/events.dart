import 'package:flutter/gestures.dart';

extension ScaleEndDetailsExtension on ScaleEndDetails {
  Map<String, dynamic> toMap() => {
        "pc": pointerCount,
        "vx": velocity.pixelsPerSecond.dx,
        "vy": velocity.pixelsPerSecond.dy,
      };
}

extension ScaleUpdateDetailsExtension on ScaleUpdateDetails {
  Map<String, dynamic> toMap() => {
        "fpx": focalPoint.dx,
        "fpy": focalPoint.dy,
        "fpdx": focalPointDelta.dx,
        "fpdy": focalPointDelta.dy,
        "lfpx": localFocalPoint.dx,
        "lfpy": localFocalPoint.dy,
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
        "fpx": focalPoint.dx,
        "fpy": focalPoint.dy,
        "lfpx": localFocalPoint.dx,
        "lfpy": localFocalPoint.dy,
        "pc": pointerCount,
        "ts": sourceTimeStamp,
      };
}

extension DragEndDetailsExtension on DragEndDetails {
  Map<String, dynamic> toMap() => {
        "lx": localPosition.dx,
        "ly": localPosition.dy,
        "gx": globalPosition.dx,
        "gy": globalPosition.dy,
        "vx": velocity.pixelsPerSecond.dx,
        "vy": velocity.pixelsPerSecond.dy,
        "pv": primaryVelocity,
      };
}

extension LongPressEndDetailsExtension on LongPressEndDetails {
  Map<String, dynamic> toMap() => {
        "lx": localPosition.dx,
        "ly": localPosition.dy,
        "gx": globalPosition.dx,
        "gy": globalPosition.dy,
        "vx": velocity.pixelsPerSecond.dx,
        "vy": velocity.pixelsPerSecond.dy,
      };
}

extension LongPressStartDetailsExtension on LongPressStartDetails {
  Map<String, dynamic> toMap() => {
        "lx": localPosition.dx,
        "ly": localPosition.dy,
        "gx": globalPosition.dx,
        "gy": globalPosition.dy,
      };
}

extension TapDownDetailsExtension on TapDownDetails {
  Map<String, dynamic> toMap() => {
        "k": kind?.name,
        "lx": localPosition.dx,
        "ly": localPosition.dy,
        "gx": globalPosition.dx,
        "gy": globalPosition.dy,
      };
}

extension TapUpDetailsExtension on TapUpDetails {
  Map<String, dynamic> toMap() => {
        "k": kind.name,
        "lx": localPosition.dx,
        "ly": localPosition.dy,
        "gx": globalPosition.dx,
        "gy": globalPosition.dy,
      };
}

extension PointerScrollEventExt on PointerScrollEvent {
  Map<String, dynamic> toMap() => {
        "lx": localPosition.dx,
        "ly": localPosition.dy,
        "gx": position.dx,
        "gy": position.dy,
        "sdx": scrollDelta.dx,
        "sdy": scrollDelta.dy,
      };
}

extension PointerEnterEventExt on PointerEnterEvent {
  Map<String, dynamic> toMap() => {
        "k": kind.name,
        "lx": localPosition.dx,
        "ly": localPosition.dy,
        "gx": position.dx,
        "gy": position.dy,
        "ts": timeStamp,
      };
}

extension PointerExitEventExt on PointerExitEvent {
  Map<String, dynamic> toMap() => {
        "k": kind.name,
        "lx": localPosition.dx,
        "ly": localPosition.dy,
        "gx": position.dx,
        "gy": position.dy,
        "ts": timeStamp,
      };
}

extension DragStartDetailsExtension on DragStartDetails {
  Map<String, dynamic> toMap() => {
        "k": kind?.name,
        "lx": localPosition.dx,
        "ly": localPosition.dy,
        "gx": globalPosition.dx,
        "gy": globalPosition.dy,
        "ts": sourceTimeStamp,
      };
}

extension DragUpdateDetailsExtension on DragUpdateDetails {
  Map<String, dynamic> toMap(double previousX, double previousY) {
    return {
      "lx": localPosition.dx,
      "ly": localPosition.dy,
      "gx": globalPosition.dx,
      "gy": globalPosition.dy,
      "ts": sourceTimeStamp,
      "dx": localPosition.dx - previousX,
      "dy": localPosition.dy - previousY,
      "pd": primaryDelta,
    };
  }
}

extension PointerHoverEventExt on PointerHoverEvent {
  Map<String, dynamic> toMap(double previousX, double previousY) {
    return {
      "k": kind.name,
      "lx": localPosition.dx,
      "ly": localPosition.dy,
      "gx": position.dx,
      "gy": position.dy,
      "ts": timeStamp,
      "dx": localPosition.dx - previousX,
      "dy": localPosition.dy - previousY,
    };
  }
}
