import 'package:awesome_notifications/awesome_notifications.dart';
import 'package:flutter/material.dart';

class NotificationService {
  static Future<void> initializeLocalNotifications(
      {required List<NotificationChannel> channels, String? languageCode, String? icon}) async {
    await AwesomeNotifications().initialize(
        icon,
        channels,
        languageCode: languageCode,
        debug: true);

    await AwesomeNotifications().isNotificationAllowed().then((isAllowed) {
      if (!isAllowed) {
        AwesomeNotifications().requestPermissionToSendNotifications();
      }
    });

    await AwesomeNotifications().setListeners(
      onActionReceivedMethod: onActionReceivedMethod,
      onDismissActionReceivedMethod: (receivedNotification) async {
        debugPrint('Notification dismissed: ${receivedNotification.id}');
      },
      onNotificationDisplayedMethod: (receivedNotification) async {
        debugPrint('Notification displayed: ${receivedNotification.id}');
      },
      onNotificationCreatedMethod: (receivedNotification) async {
        debugPrint('Notification created: ${receivedNotification.id}');
      },
    );
  }

  static Future<void> onActionReceivedMethod(
      ReceivedAction receivedAction) async {
    debugPrint('Notification Action received');
  }

  static void showNotification(NotificationContent content,
      {List<NotificationActionButton>? actionButtons, NotificationSchedule? schedule}) {
    AwesomeNotifications().createNotification(
      content: content,
      actionButtons: actionButtons,
      schedule: schedule,
    );
  }
}
