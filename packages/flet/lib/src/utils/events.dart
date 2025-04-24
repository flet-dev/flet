import 'package:flutter/gestures.dart';

extension ScaleEndDetailsExtension on ScaleEndDetails {
  Map<String, dynamic> toMap() => {
        "pointer_count": pointerCount,
        "velocity_x": velocity.pixelsPerSecond.dx,
        "velocity_y": velocity.pixelsPerSecond.dy,
      };
}

extension ScaleUpdateDetailsExtension on ScaleUpdateDetails {
  Map<String, dynamic> toMap() => {
        "focal_point_x": focalPoint.dx,
        "focal_point_y": focalPoint.dy,
        "focal_point_delta_x": focalPointDelta.dx,
        "focal_point_delta_y": focalPointDelta.dy,
        "local_focal_point_x": localFocalPoint.dx,
        "local_focal_point_y": localFocalPoint.dy,
        "pointer_count": pointerCount,
        "horizontal_scale": horizontalScale,
        "vertical_scale": verticalScale,
        "scale": scale,
        "rotation": rotation,
        "timestamp": sourceTimeStamp,
      };
}

extension ScaleStartDetailsExtension on ScaleStartDetails {
  Map<String, dynamic> toMap() => {
        "focal_point_x": focalPoint.dx,
        "focal_point_y": focalPoint.dy,
        "local_focal_point_x": localFocalPoint.dx,
        "local_focal_point_y": localFocalPoint.dy,
        "pointer_count": pointerCount,
        "timestamp": sourceTimeStamp,
      };
}

extension DragEndDetailsExtension on DragEndDetails {
  Map<String, dynamic> toMap() => {
        "local_x": localPosition.dx,
        "local_y": localPosition.dy,
        "global_x": globalPosition.dx,
        "global_y": globalPosition.dy,
        "velocity_x": velocity.pixelsPerSecond.dx,
        "velocity_y": velocity.pixelsPerSecond.dy,
        "primary_velocity": primaryVelocity,
      };
}

extension LongPressEndDetailsExtension on LongPressEndDetails {
  Map<String, dynamic> toMap() => {
        "local_x": localPosition.dx,
        "local_y": localPosition.dy,
        "global_x": globalPosition.dx,
        "global_y": globalPosition.dy,
        "velocity_x": velocity.pixelsPerSecond.dx,
        "velocity_y": velocity.pixelsPerSecond.dy,
      };
}

extension LongPressStartDetailsExtension on LongPressStartDetails {
  Map<String, dynamic> toMap() => {
        "local_x": localPosition.dx,
        "local_y": localPosition.dy,
        "global_x": globalPosition.dx,
        "global_y": globalPosition.dy,
      };
}

extension TapDownDetailsExtension on TapDownDetails {
  Map<String, dynamic> toMap() => {
        "kind": kind?.name,
        "local_x": localPosition.dx,
        "local_y": localPosition.dy,
        "global_x": globalPosition.dx,
        "global_y": globalPosition.dy,
      };
}

extension TapUpDetailsExtension on TapUpDetails {
  Map<String, dynamic> toMap() => {
        "kind": kind.name,
        "local_x": localPosition.dx,
        "local_y": localPosition.dy,
        "global_x": globalPosition.dx,
        "global_y": globalPosition.dy,
      };
}

extension PointerScrollEventExt on PointerScrollEvent {
  Map<String, dynamic> toMap() => {
        "local_x": localPosition.dx,
        "local_y": localPosition.dy,
        "global_x": position.dx,
        "global_y": position.dy,
        "scroll_delta_x": scrollDelta.dx,
        "scroll_delta_y": scrollDelta.dy,
      };
}

extension PointerEnterEventExt on PointerEnterEvent {
  Map<String, dynamic> toMap() => {
        "kind": kind.name,
        "local_x": localPosition.dx,
        "local_y": localPosition.dy,
        "global_x": position.dx,
        "global_y": position.dy,
        "timestamp": timeStamp,
      };
}

extension PointerExitEventExt on PointerExitEvent {
  Map<String, dynamic> toMap() => {
        "kind": kind.name,
        "local_x": localPosition.dx,
        "local_y": localPosition.dy,
        "global_x": position.dx,
        "global_y": position.dy,
        "timestamp": timeStamp,
      };
}

extension DragStartDetailsExtension on DragStartDetails {
  Map<String, dynamic> toMap() => {
        "kind": kind?.name,
        "local_x": localPosition.dx,
        "local_y": localPosition.dy,
        "global_x": globalPosition.dx,
        "global_y": globalPosition.dy,
        "timestamp": sourceTimeStamp,
      };
}

extension DragUpdateDetailsExtension on DragUpdateDetails {
  Map<String, dynamic> toMap(double previousX, double previousY) {
    return {
      "local_x": localPosition.dx,
      "local_y": localPosition.dy,
      "global_x": globalPosition.dx,
      "global_y": globalPosition.dy,
      "timestamp": sourceTimeStamp,
      "delta_x": localPosition.dx - previousX,
      "delta_y": localPosition.dy - previousY,
      "primary_delta": primaryDelta,
    };
  }
}

extension PointerHoverEventExt on PointerHoverEvent {
  Map<String, dynamic> toMap(double previousX, double previousY) {
    return {
      "kind": kind.name,
      "local_x": localPosition.dx,
      "local_y": localPosition.dy,
      "global_x": position.dx,
      "global_y": position.dy,
      "timestamp": timeStamp,
      "delta_x": localPosition.dx - previousX,
      "delta_y": localPosition.dy - previousY,
    };
  }
}
