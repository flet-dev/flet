import 'dart:convert';

/// Launch arguments for a Windows notification or one of its buttons.
///
/// Windows hands the app a clicked element's launch arguments and nothing else:
/// the plugin reports a click on the notification's body as an action too, with
/// the arguments as its action id, and without the notification's id. Encoding
/// them lets [decodeWindowsLaunchArguments] tell the two apart and restore the
/// id and payload.
String windowsLaunchArguments({
  required int? notificationId,
  required String? payload,
  String? actionId,
}) =>
    jsonEncode({
      "notification": notificationId,
      if (actionId != null) "id": actionId,
      "payload": payload,
    });

/// Decodes [windowsLaunchArguments], or returns `null` for other strings, such
/// as action ids on other platforms.
({int? notificationId, String? actionId, String? payload})?
    decodeWindowsLaunchArguments(String? arguments) {
  if (arguments == null || !arguments.startsWith("{")) return null;
  try {
    final decoded = jsonDecode(arguments);
    if (decoded is! Map || !decoded.containsKey("notification")) return null;
    return (
      notificationId: decoded["notification"] as int?,
      actionId: decoded["id"] as String?,
      payload: decoded["payload"] as String?,
    );
  } on FormatException {
    return null;
  }
}
