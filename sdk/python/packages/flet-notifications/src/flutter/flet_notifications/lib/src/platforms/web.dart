import 'package:flet/flet.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

import '../utils/actions.dart';

/// Builds the web details of a notification from a `WebOptions` payload.
fln.WebNotificationDetails parseWebDetails({
  required List<ParsedAction> actions,
  Map<dynamic, dynamic>? options,
}) {
  final webOptions = options ?? const {};
  return fln.WebNotificationDetails(
    actions: actions
        .map((a) => fln.WebNotificationAction(action: a.id, title: a.title))
        .toList(),
    direction: parseEnum(
      fln.WebNotificationDirection.values,
      webOptions["direction"] as String?,
      fln.WebNotificationDirection.auto,
    )!,
    badgeUrl: webOptions["badge_url"] == null
        ? null
        : Uri.parse(webOptions["badge_url"] as String),
    iconUrl: webOptions["icon_url"] == null
        ? null
        : Uri.parse(webOptions["icon_url"] as String),
    imageUrl: webOptions["image_url"] == null
        ? null
        : Uri.parse(webOptions["image_url"] as String),
    lang: webOptions["lang"] as String?,
    requireInteraction: parseBool(webOptions["require_interaction"], false)!,
    isSilent: parseBool(webOptions["silent"], false)!,
    renotify: parseBool(webOptions["renotify"], false)!,
    timestamp: webOptions["timestamp"] as DateTime?,
  );
}
