import 'package:flutter/widgets.dart';

import '../flet_backend.dart';
import '../models/control.dart';

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
    _onScrollInterval = widget.control.get<int>("on_scroll_interval", 10)!;

    return NotificationListener<ScrollNotification>(
      child: widget.child,
      onNotification: (notification) => _onNotification(notification, context),
    );
  }

  bool _onNotification(ScrollNotification notification, BuildContext context) {
    if (notification.depth == 0) {
      var eventType = notification.runtimeType.toString();
      var now = DateTime.now().millisecondsSinceEpoch;
      var lastEventTimestamp = _lastEventTimestamps[eventType];
      if (lastEventTimestamp == null ||
          now - lastEventTimestamp > _onScrollInterval) {
        _lastEventTimestamps[eventType] = now;

        Map<String, Object?> data = {
          "pixels": notification.metrics.pixels,
          "min_scroll_extent": notification.metrics.minScrollExtent,
          "max_scroll_extent": notification.metrics.maxScrollExtent,
          "viewport_dimension": notification.metrics.viewportDimension
        };
        if (notification is ScrollStartNotification) {
          data["event_type"] = "start";
        } else if (notification is ScrollUpdateNotification) {
          data["event_type"] = "update";
          data["scroll_delta"] = notification.scrollDelta;
        } else if (notification is ScrollEndNotification) {
          data["event_type"] = "end";
        } else if (notification is UserScrollNotification) {
          data["event_type"] = "user";
          data["direction"] = notification.direction.name;
        } else if (notification is OverscrollNotification) {
          data["event_type"] = "over";
          data["overscroll"] = notification.overscroll;
          data["velocity"] = notification.velocity;
        }

        if (data["event_type"] != null) {
          debugPrint("ScrollNotification ${widget.control.id} event");
          FletBackend.of(context)
              .triggerControlEvent(widget.control, "scroll", data);
        }
      }
    }

    return false;
  }
}
