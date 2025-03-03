import 'package:awesome_notifications/awesome_notifications.dart';
import 'package:flet/flet.dart';
import 'package:flet_notifications/src/service.dart';
import 'package:flutter/material.dart';

import 'notifications.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "notifications":
      return NotificationControl(
          parent: args.parent,
          control: args.control,
          nextChild: args.nextChild,
          backend: args.backend);
    default:
      return null;
  }
};

void ensureInitialized() async{
  await NotificationService.initializeLocalNotifications(
    channels: [
          NotificationChannel(
              channelKey: 'alerts',
              channelName: 'Notification Channel Name',
              channelDescription: 'Notification Channel Description',
              playSound: true,
              onlyAlertOnce: true,
              groupAlertBehavior: GroupAlertBehavior.Children,
              importance: NotificationImportance.High,
              defaultPrivacy: NotificationPrivacy.Private,
              defaultColor: Colors.deepPurple,
              ledColor: Colors.deepPurple)
        ]
  );
}
