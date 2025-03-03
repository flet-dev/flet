import 'package:flet/flet.dart';
import 'package:flet_notifications/src/utils/notifications.dart';
import 'package:flutter/material.dart';

import 'service.dart';

class NotificationControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final Widget? nextChild;
  final FletControlBackend backend;

  const NotificationControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.nextChild,
      required this.backend});

  @override
  State<NotificationControl> createState() => _NotificationControlState();
}

class _NotificationControlState extends State<NotificationControl>
    with FletStoreMixin {
  @override
  void initState() {
    super.initState();
    Future.microtask(() => _initializeService());
  }

  Future<void> _initializeService() async {
    var channels = parseNotificationChannels(
        widget.control, "channels", Theme.of(context));
    await NotificationService.initializeLocalNotifications(
      channels: channels,
      languageCode: widget.control.attrString("languageCode"),
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "Notification build: ${widget.control.id} (${widget.control.hashCode})");

    () async {
      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "show":
            var content =
                notificationContentFromJSON(Theme.of(context), args["content"]);
            var actionButtons = notificationActionButtonsFromJSON(
                Theme.of(context), args["action_buttons"]);
            if (content != null) {
              debugPrint("NotificationService.showNotification");
              NotificationService.showNotification(content,
                  actionButtons: actionButtons);
            }
        }
        return null;
      });
    }();

    return const SizedBox.shrink();
  }
}
