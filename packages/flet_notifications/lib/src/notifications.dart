import 'dart:convert';

import 'package:awesome_notifications/awesome_notifications.dart';
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
      icon: widget.control.attrString("icon"),
    );
  }

  @override
  void dispose() {
    AwesomeNotifications().dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "Notifications build: ${widget.control.id} (${widget.control.hashCode})");

    () async {
      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "show":
            var content =
                notificationContentFromJSON(Theme.of(context), args["content"]);
            var actionButtons = notificationActionButtonsFromJSON(
                Theme.of(context), args["action_buttons"]);
            var schedule = args["schedule"] != null
                ? args["schedule_parser"] == "interval"
                    ? notificationIntervalFromJSON(args["schedule"],
                        jsonDecode: true)
                    : notificationCalendarFromJSON(args["schedule"],
                        jsonDecode: true)
                : null;
            if (content != null) {
              debugPrint("NotificationService.showNotification");
              NotificationService.showNotification(content,
                  actionButtons: actionButtons, schedule: schedule);
            }
          // dismissals
          case "dismiss":
            var id = parseInt(args["id"]);
            var channelKey = args["channel_key"];
            var groupKey = args["group_key"];
            if (id != null) {
              await AwesomeNotifications().dismiss(id);
            } else if (channelKey != null) {
              await AwesomeNotifications()
                  .dismissNotificationsByChannelKey(channelKey);
            } else if (groupKey != null) {
              await AwesomeNotifications()
                  .dismissNotificationsByGroupKey(groupKey);
            }
            break;
          case "dismiss_all":
            await AwesomeNotifications().dismissAllNotifications();

          // cancellations
          case "cancel":
            var id = parseInt(args["id"]);
            var channelKey = args["channel_key"];
            var groupKey = args["group_key"];
            if (id != null) {
              await AwesomeNotifications().cancelSchedule(id);
            } else if (channelKey != null) {
              await AwesomeNotifications()
                  .cancelNotificationsByChannelKey(channelKey);
            } else if (groupKey != null) {
              await AwesomeNotifications()
                  .cancelNotificationsByGroupKey(groupKey);
            }
            break;
          case "cancel_schedule":
            var id = parseInt(args["id"]);
            var channelKey = args["channel_key"];
            var groupKey = args["group_key"];
            if (id != null) {
              await AwesomeNotifications().cancelSchedule(id);
            } else if (channelKey != null) {
              await AwesomeNotifications()
                  .cancelSchedulesByChannelKey(channelKey);
            } else if (groupKey != null) {
              await AwesomeNotifications().cancelSchedulesByGroupKey(groupKey);
            }
            break;
          case "cancel_all_schedules":
            await AwesomeNotifications().cancelAllSchedules();
            break;

          // badge_counter
          case "get_badge_counter":
            return await AwesomeNotifications()
                .getGlobalBadgeCounter()
                .then((value) => value.toString());
          case "set_badge_counter":
            var value = parseInt(args["value"]);
            if (value != null) {
              await AwesomeNotifications().setGlobalBadgeCounter(value);
            }
            break;
          case "increment_badge_counter":
            return await AwesomeNotifications()
                .incrementGlobalBadgeCounter()
                .then((value) => value.toString());
          case "decrement_badge_counter":
            return await AwesomeNotifications()
                .decrementGlobalBadgeCounter()
                .then((value) => value.toString());
          case "reset_badge_counter":
            await AwesomeNotifications().resetGlobalBadge();
            break;

          // channels
          case "set_channel":
            var notificationChannel = notificationChannelFromJSON(
                Theme.of(context), args["channel"],
                jsonDecode: true);
            if (notificationChannel != null) {
              await AwesomeNotifications().setChannel(notificationChannel,
                  forceUpdate: parseBool(args["force_update"], false)!);
            }
            break;
          case "remove_channel":
            var channelKey = args["channel_key"];
            if (channelKey != null) {
              await AwesomeNotifications().removeChannel(channelKey);
            }
            break;

          // permissions
          case "is_allowed":
            return await AwesomeNotifications()
                .isNotificationAllowed()
                .then((value) => value.toString());
          case "request_permission":
            return await AwesomeNotifications()
                .requestPermissionToSendNotifications()
                .then((value) => value.toString());

          // time
          case "get_local_timezone_identifier":
            return await AwesomeNotifications()
                .getLocalTimeZoneIdentifier()
                .then((value) => value);
          case "get_next_date":
            return "";
          case "get_utc_timezone_identifier":
            return await AwesomeNotifications()
                .getUtcTimeZoneIdentifier()
                .then((value) => value);

          // others
          case "show_alarm_page":
            await AwesomeNotifications().showAlarmPage();
            break;
          case "get_initial_action":
            return await AwesomeNotifications()
                .getInitialNotificationAction(
                    removeFromActionEvents:
                        parseBool(args["remove_from_action_events"], false)!)
                .then((ReceivedAction? action) => jsonEncode(action?.toMap()));
          case "show_global_dnd_override_page":
            await AwesomeNotifications().showGlobalDndOverridePage();
            break;

          case "get_lifecycle":
            return await AwesomeNotifications()
                .getAppLifeCycle()
                .then((value) => value.name.toLowerCase());
          case "get_localization":
            return await AwesomeNotifications()
                .getLocalization()
                .then((value) => value);
          case "is_active_on_status_bar":
            var id = parseInt(args["id"]);
            if (id != null) {
              return await AwesomeNotifications()
                  .isNotificationActiveOnStatusBar(id: id)
                  .then((value) => value.toString());
            }
            break;

          case "get_ids_active_on_status_bar":
            return await AwesomeNotifications()
                .getAllActiveNotificationIdsOnStatusBar()
                .then((value) => jsonEncode(value));
        }
        return null;
      });
    }();

    return const SizedBox.shrink();
  }
}
