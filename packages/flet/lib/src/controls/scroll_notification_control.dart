import 'package:flutter/widgets.dart';

import '../models/control.dart';
import '../utils/numbers.dart';

class ScrollNotificationControl extends StatefulWidget {
  final Widget child;
  final Control control;

  const ScrollNotificationControl(
      {super.key, required this.child, required this.control});

  @override
  State<ScrollNotificationControl> createState() =>
      _ScrollNotificationControlState();
}

class _ScrollNotificationControlState extends State<ScrollNotificationControl> {
  int _onScrollInterval = 0;
  final Map<String, int> _lastEventTimestamps = {};

  @override
  Widget build(BuildContext context) {
    _onScrollInterval = widget.control.getInt("on_scroll_interval", 10)!;

    return NotificationListener<ScrollNotification>(
      child: widget.child,
      onNotification: (notification) => _onNotification(notification, context),
    );
  }

  bool _onNotification(ScrollNotification notification, BuildContext context) {
    if (notification.depth != 0) return false;

    final eventType = notification.runtimeType.toString();
    final now = DateTime.now().millisecondsSinceEpoch;
    final lastEventTimestamp = _lastEventTimestamps[eventType];

    if (lastEventTimestamp != null &&
        now - lastEventTimestamp <= _onScrollInterval) {
      return false;
    }

    _lastEventTimestamps[eventType] = now;

    final metrics = notification.metrics;
    final Map<String, Object?> fields = {
      "pixels": metrics.pixels,
      "min_scroll_extent": metrics.minScrollExtent,
      "max_scroll_extent": metrics.maxScrollExtent,
      "viewport_dimension": metrics.viewportDimension,
    };

    if (notification is ScrollStartNotification) {
      fields["event_type"] = "start";
    } else if (notification is ScrollUpdateNotification) {
      fields["event_type"] = "update";
      fields["scroll_delta"] = notification.scrollDelta;
    } else if (notification is ScrollEndNotification) {
      fields["event_type"] = "end";
    } else if (notification is UserScrollNotification) {
      fields["event_type"] = "user";
      fields["direction"] = notification.direction.name;
    } else if (notification is OverscrollNotification) {
      fields["event_type"] = "overscroll";
      fields["overscroll"] = notification.overscroll;
      fields["velocity"] = notification.velocity;
    }

    // Check that event_type was set before triggering the event
    if (fields["event_type"] != null) {
      debugPrint("ScrollNotification ${widget.control.id} event");
      widget.control.triggerEvent("scroll", fields: fields);
    }

    return false;
  }
}
