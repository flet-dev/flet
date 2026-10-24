/// Error codes Python maps to its notification exception classes.
enum NotificationErrorCode {
  unsupportedPlatform("unsupported_platform"),
  initializationFailed("initialization_failed"),
  invalidArgument("invalid_argument"),
  permissionDenied("permission_denied"),
  operationFailed("operation_failed");

  const NotificationErrorCode(this.value);

  /// Serialized code matching the Python enum's value.
  final String value;
}

/// A notification failure with a code understood by the Python API.
///
/// Flet reports a failed method call to Python with the exception's text, so
/// [toString] leads with the code for Python to map back to a
/// `NotificationException` subclass.
class NotificationException implements Exception {
  const NotificationException(this.code, this.message);

  const NotificationException.unsupportedPlatform(String message)
      : this(NotificationErrorCode.unsupportedPlatform, message);

  const NotificationException.initializationFailed(String message)
      : this(NotificationErrorCode.initializationFailed, message);

  const NotificationException.invalidArgument(String message)
      : this(NotificationErrorCode.invalidArgument, message);

  const NotificationException.permissionDenied(String message)
      : this(NotificationErrorCode.permissionDenied, message);

  const NotificationException.operationFailed(String message)
      : this(NotificationErrorCode.operationFailed, message);

  final NotificationErrorCode code;
  final String message;

  @override
  String toString() => "${code.value}: $message";
}
