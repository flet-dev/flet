import 'package:flutter/widgets.dart';

import '../flet_backend.dart';
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
    if (notification.depth == 0) {
      var eventType = notification.runtimeType.toString();
      var now = DateTime.now().millisecondsSinceEpoch;
      var lastEventTimestamp = _lastEventTimestamps[eventType];
      if (lastEventTimestamp == null ||
          now - lastEventTimestamp > _onScrollInterval) {
        _lastEventTimestamps[eventType] = now;

        Map<String, Object?> data = {
          "p": notification.metrics.pixels,
          "minse": notification.metrics.minScrollExtent,
          "maxse": notification.metrics.maxScrollExtent,
          "vd": notification.metrics.viewportDimension
        };
        if (notification is ScrollStartNotification) {
          data["t"] = "start";
        } else if (notification is ScrollUpdateNotification) {
          data["t"] = "update";
          data["sd"] = notification.scrollDelta;
        } else if (notification is ScrollEndNotification) {
          data["t"] = "end";
        } else if (notification is UserScrollNotification) {
          data["t"] = "user";
          data["dir"] = notification.direction.name;
        } else if (notification is OverscrollNotification) {
          data["t"] = "overscroll";
          data["os"] = notification.overscroll;
          data["v"] = notification.velocity;
        }

        if (data["t"] != null) {
          debugPrint("ScrollNotification ${widget.control.id} event");
           widget.control.triggerEvent("scroll", data);
        }
      }
    }

    return false;
  }
}
