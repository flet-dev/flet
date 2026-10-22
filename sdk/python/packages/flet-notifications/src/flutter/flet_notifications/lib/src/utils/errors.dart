/// Error categories shared with the Python notification API.
enum NotificationErrorCode {
  unsupportedPlatform("unsupported_platform"),
  initFailed("init_failed"),
  showFailed("show_failed"),
  cancelFailed("cancel_failed"),
  scheduleFailed("schedule_failed"),
  invalidAction("invalid_action"),
  invalidSchedule("invalid_schedule"),
  invalidStyle("invalid_style"),
  invalidChannel("invalid_channel"),
  invalidServiceId("invalid_service_id"),
  invalidOption("invalid_option"),
  channelFailed("channel_failed"),
  foregroundServiceFailed("foreground_service_failed"),
  queryFailed("query_failed"),
  permissionFailed("permission_failed"),
  unknownMethod("unknown_method");

  const NotificationErrorCode(this.value);

  /// Serialized code used by Python's NotificationErrorCode constants.
  final String value;
}

/// A notification failure with a code understood by the Python API.
class NotificationException implements Exception {
  const NotificationException(this.code, this.message);

  const NotificationException.initFailed(String message)
      : this(NotificationErrorCode.initFailed, message);

  const NotificationException.invalidAction(String message)
      : this(NotificationErrorCode.invalidAction, message);

  const NotificationException.invalidChannel(String message)
      : this(NotificationErrorCode.invalidChannel, message);

  const NotificationException.invalidOption(String message)
      : this(NotificationErrorCode.invalidOption, message);

  const NotificationException.invalidSchedule(String message)
      : this(NotificationErrorCode.invalidSchedule, message);

  const NotificationException.invalidServiceId(String message)
      : this(NotificationErrorCode.invalidServiceId, message);

  const NotificationException.invalidStyle(String message)
      : this(NotificationErrorCode.invalidStyle, message);

  const NotificationException.unknownMethod(String message)
      : this(NotificationErrorCode.unknownMethod, message);

  const NotificationException.unsupportedPlatform(String message)
      : this(NotificationErrorCode.unsupportedPlatform, message);

  final NotificationErrorCode code;
  final String message;

  /// Encodes the failure for the Python invocation result.
  String toResult() => "error:${code.value}:$message";

  @override
  String toString() => "${code.value}: $message";
}
