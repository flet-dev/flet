import 'dart:convert';

import 'package:awesome_notifications/awesome_notifications.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

NotificationContent? parseNotificationContent(
    Control control, String propName, ThemeData theme,
    [NotificationContent? defValue]) {
  var v = control.attrString(propName);
  if (v == null) {
    return defValue;
  }
  final j1 = json.decode(v);
  return notificationContentFromJSON(j1, theme, defValue);
}

NotificationContent? notificationContentFromJSON(ThemeData theme, dynamic j,
    [NotificationContent? defValue]) {
  j = j != null ? json.decode(j) : null;
  var id = parseInt(j['id']);
  var channelKey = j['channel_key'];

  if (j == null || id == null || channelKey == null) {
    return defValue;
  }

  return NotificationContent(
    id: id,
    channelKey: channelKey,
    title: j["title"],
    body: j["body"],
    titleLocKey: j["title_loc_key"],
    bodyLocKey: j["body_loc_key"],
    //titleLocArgs: ,
    //bodyLocArgs:,
    groupKey: j["group_key"],
    summary: j["summary"],
    icon: j["icon"],
    largeIcon: j["large_icon"],
    bigPicture: j["big_picture"],
    customSound: j["custom_sound"],
    showWhen: parseBool(j["show_when"], true)!,
    wakeUpScreen: parseBool(j["wake_up_screen"], false)!,
    fullScreenIntent: parseBool(j["full_screen_intent"], false)!,
    criticalAlert: parseBool(j["critical_alert"], false)!,
    roundedLargeIcon: parseBool(j["rounded_large_icon"], false)!,
    roundedBigPicture: parseBool(j["rounded_big_picture"], false)!,
    autoDismissible: parseBool(j["auto_dismissible"], true)!,
    color: parseColor(theme, j["color"]),
    timeoutAfter: durationFromJSON(j["timeout_after"]),
    chronometer: durationFromJSON(j["chronometer"]),
    backgroundColor: parseColor(theme, j["bgcolor"]),
    hideLargeIconOnExpand: parseBool(j["hide_large_icon_on_expand"], false)!,
    locked: parseBool(j["locked"], false)!,
    progress: parseDouble(j["progress"]),
    badge: parseInt(j["badge"]),
    ticker: j["ticker"],
    displayOnForeground: parseBool(j["display_on_foreground"], true)!,
    displayOnBackground: parseBool(j["display_on_background"], true)!,
    duration: durationFromJSON(j["duration"]),
    playbackSpeed: parseDouble(j["playback_speed"]),
    actionType: parseActionType(j["action_type"], ActionType.Default)!,
    category: parseNotificationCategory(j["category"]),
    notificationLayout:
        parseNotificationLayout(j["layout"], NotificationLayout.Default)!,
  );
}

NotificationActionButton? notificationActionButtonFromJSON(
    ThemeData theme, dynamic j,
    [NotificationActionButton? defValue]) {
  var key = j?['key'];
  var label = j?['label'];

  if (j == null || key == null || label == null) {
    return defValue;
  }

  return NotificationActionButton(
    key: key,
    label: label,
    enabled: !parseBool(j["disabled"], false)!,
    isAuthenticationRequired: parseBool(j["requires_authentication"], false)!,
    isDangerousOption: parseBool(j["dangerous"], false)!,
    requireInputText: parseBool(j["require_text_input"], false)!,
    showInCompactView: parseBool(j["show_in_compact_view"], true)!,
    autoDismissible: parseBool(j["auto_dismissible"], true)!,
    color: parseColor(theme, j["color"]),
    icon: j["icon"],
    actionType: parseActionType(j["action_type"], ActionType.Default)!,
  );
}

List<NotificationActionButton>? notificationActionButtonsFromJSON(
    ThemeData theme, dynamic j,
    [List<NotificationActionButton>? defValue]) {
  j = j != null ? json.decode(j) : null;
  if (j == null) return defValue;

  var buttons = <NotificationActionButton>[];
  for (var b in j) {
    var actionButton = notificationActionButtonFromJSON(theme, b);
    if (actionButton != null) {
      buttons.add(actionButton);
    }
  }
  return buttons;
}

List<NotificationChannel> parseNotificationChannels(
    Control control, String propName, ThemeData theme,
    [List<NotificationChannel>? defValue]) {
  var v = control.attrString(propName);
  if (v == null) {
    return defValue ?? [];
  }

  final List<dynamic> jsonList = json.decode(v);
  if (jsonList.isEmpty) {
    return defValue ?? [];
  }

  List<NotificationChannel> channels = [];
  for (var j in jsonList) {
    var channel = notificationChannelFromJSON(theme, j);
    if (channel != null) {
      channels.add(channel);
    }
  }

  return channels;
}

NotificationChannel? notificationChannelFromJSON(ThemeData theme, dynamic j,
    {NotificationChannel? defValue, bool jsonDecode = false}) {
  if (jsonDecode && j is String) {
    j = json.decode(j);
  }
  var channelKey = j?['channel_key'];
  var channelName = j?['channel_name'];
  var channelDescription = j?['channel_description'];

  if (j == null ||
      channelKey == null ||
      channelName == null ||
      channelDescription == null) {
    return defValue;
  }

  return NotificationChannel(
    channelKey: channelKey,
    channelName: channelName,
    channelDescription: channelDescription,
    channelGroupKey: j["channel_group_key"],
    channelShowBadge: parseBool(j["channel_show_badge"]),
    criticalAlerts: parseBool(j["critical_alerts"]),
    defaultColor: parseColor(theme, j["default_color"]),
    enableLights: parseBool(j["enable_lights"]),
    enableVibration: parseBool(j["enable_vibration"]),
    ledColor: parseColor(theme, j["led_color"]),
    ledOnMs: parseInt(j["led_on_ms"]),
    ledOffMs: parseInt(j["led_off_ms"]),
    onlyAlertOnce: parseBool(j["only_alert_once"]),
    playSound: parseBool(j["play_sound"]),
    soundSource: j["sound_source"],
    groupKey: j["group_key"],
    icon: j["icon"],
    locked: parseBool(j["locked"], false)!,
    defaultPrivacy: parseNotificationPrivacy(j["privacy"]),
    groupSort: parseGroupSort(j["group_sort"]),
    importance: parseNotificationImportance(j["importance"]),
    defaultRingtoneType: parseRingtoneType(j["ringtone_type"]),
    groupAlertBehavior: parseGroupAlertBehavior(j["group_alert_behavior"]),
  );
}

NotificationCalendar? notificationCalendarFromJSON(dynamic j,
    {NotificationCalendar? defValue, bool jsonDecode = false}) {
  if (jsonDecode && j is String) {
    j = json.decode(j);
  }

  if (j == null) {
    return defValue;
  }

  return NotificationCalendar(
    allowWhileIdle: parseBool(j["allow_while_idle"], false)!,
    preciseAlarm: parseBool(j["precise_alarm"], false)!,
    repeats: parseBool(j["repeats"], false)!,
    timeZone: j["time_zone"],
    day: parseInt(j["day"]),
    hour: parseInt(j["hour"]),
    minute: parseInt(j["minute"]),
    second: parseInt(j["second"]),
    millisecond: parseInt(j["millisecond"]),
    month: parseInt(j["month"]),
    weekday: parseInt(j["weekday"]),
    weekOfYear: parseInt(j["week_of_year"]),
    year: parseInt(j["year"]),
    era: parseInt(j["era"]),
    // weekOfMonth (not fully implemented atm)
  );
}

NotificationInterval? notificationIntervalFromJSON(dynamic j,
    {NotificationInterval? defValue, bool jsonDecode = false}) {
  if (jsonDecode && j is String) {
    j = json.decode(j);
  }

  if (j == null || j["interval"] == null) {
    return defValue;
  }

  return NotificationInterval(
    interval: durationFromJSON(j["interval"]),
    allowWhileIdle: parseBool(j["allow_while_idle"], false)!,
    preciseAlarm: parseBool(j["precise_alarm"], false)!,
    repeats: parseBool(j["repeats"], false)!,
    timeZone: j["time_zone"],
  );
}

ActionType? parseActionType(String? value, [ActionType? defaultActionType]) {
  if (value == null) {
    return defaultActionType;
  }
  const Map<String, ActionType> actionMap = {
    'default': ActionType.Default,
    'disabled': ActionType.DisabledAction,
    'keepontop': ActionType.KeepOnTop,
    'silent': ActionType.SilentAction,
    'silentbackground': ActionType.SilentBackgroundAction,
    'dismiss': ActionType.DismissAction,
  };
  return actionMap[value.toLowerCase()] ?? defaultActionType;
}

NotificationCategory? parseNotificationCategory(String? value,
    [NotificationCategory? defValue]) {
  if (value == null) {
    return defValue;
  }
  const Map<String, NotificationCategory> categoryMap = {
    'alarm': NotificationCategory.Alarm,
    'call': NotificationCategory.Call,
    'email': NotificationCategory.Email,
    'error': NotificationCategory.Error,
    'event': NotificationCategory.Event,
    'localsharing': NotificationCategory.LocalSharing,
    'message': NotificationCategory.Message,
    'missedcall': NotificationCategory.MissedCall,
    'navigation': NotificationCategory.Navigation,
    'progress': NotificationCategory.Progress,
    'promo': NotificationCategory.Promo,
    'recommendation': NotificationCategory.Recommendation,
    'reminder': NotificationCategory.Reminder,
    'service': NotificationCategory.Service,
    'social': NotificationCategory.Social,
    'status': NotificationCategory.Status,
    'stopwatch': NotificationCategory.StopWatch,
    'transport': NotificationCategory.Transport,
    'workout': NotificationCategory.Workout,
  };
  return categoryMap[value.toLowerCase()] ?? defValue;
}

NotificationLayout? parseNotificationLayout(String? value,
    [NotificationLayout? defValue]) {
  if (value == null) {
    return defValue;
  }
  const Map<String, NotificationLayout> layoutMap = {
    'default': NotificationLayout.Default,
    'bigpicture': NotificationLayout.BigPicture,
    'bigtext': NotificationLayout.BigText,
    'inbox': NotificationLayout.Inbox,
    'progressbar': NotificationLayout.ProgressBar,
    'messaging': NotificationLayout.Messaging,
    'messaginggroup': NotificationLayout.MessagingGroup,
    'mediaplayer': NotificationLayout.MediaPlayer,
  };
  return layoutMap[value.toLowerCase()] ?? defValue;
}

NotificationPrivacy? parseNotificationPrivacy(String? value,
    [NotificationPrivacy? defValue]) {
  if (value == null) {
    return defValue;
  }
  const Map<String, NotificationPrivacy> privacyMap = {
    'secret': NotificationPrivacy.Secret,
    'private': NotificationPrivacy.Private,
    'public': NotificationPrivacy.Public,
  };
  return privacyMap[value.toLowerCase()] ?? defValue;
}

GroupSort? parseGroupSort(String? value, [GroupSort? defValue]) {
  if (value == null) {
    return defValue;
  }
  const Map<String, GroupSort> groupSortMap = {
    'ascending': GroupSort.Asc,
    'descending': GroupSort.Desc,
  };
  return groupSortMap[value.toLowerCase()] ?? defValue;
}

NotificationImportance? parseNotificationImportance(String? value,
    [NotificationImportance? defValue]) {
  if (value == null) {
    return defValue;
  }
  const Map<String, NotificationImportance> importanceMap = {
    'none': NotificationImportance.None,
    'default': NotificationImportance.Default,
    'max': NotificationImportance.Max,
    'minimum': NotificationImportance.Min,
    'high': NotificationImportance.High,
    'low': NotificationImportance.Low,
  };
  return importanceMap[value.toLowerCase()] ?? defValue;
}

DefaultRingtoneType? parseRingtoneType(String? value,
    [DefaultRingtoneType? defValue]) {
  if (value == null) {
    return defValue;
  }
  const Map<String, DefaultRingtoneType> ringtoneMap = {
    'alarm': DefaultRingtoneType.Alarm,
    'notification': DefaultRingtoneType.Notification,
    'ringtone': DefaultRingtoneType.Ringtone,
  };
  return ringtoneMap[value.toLowerCase()] ?? defValue;
}

GroupAlertBehavior? parseGroupAlertBehavior(String? value,
    [GroupAlertBehavior? defValue]) {
  if (value == null) {
    return defValue;
  }
  const Map<String, GroupAlertBehavior> behaviorMap = {
    'all': GroupAlertBehavior.All,
    'summary': GroupAlertBehavior.Summary,
    'children': GroupAlertBehavior.Children,
  };
  return behaviorMap[value.toLowerCase()] ?? defValue;
}
