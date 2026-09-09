import 'package:local_auth/local_auth.dart';
import 'package:local_auth_android/local_auth_android.dart';
import 'package:local_auth_darwin/local_auth_darwin.dart';
import 'package:local_auth_windows/local_auth_windows.dart';

AndroidAuthMessages? parseAndroidAuthMessages(Map? value) {
  if (value == null) {
    return null;
  }
  return AndroidAuthMessages(
    signInHint: value["sign_in_hint"],
    cancelButton: value["cancel_button"],
    signInTitle: value["sign_in_title"],
  );
}

IOSAuthMessages? parseIosAuthMessages(Map? value) {
  if (value == null) {
    return null;
  }
  return IOSAuthMessages(
    cancelButton: value["cancel_button"],
    localizedFallbackTitle: value["localized_fallback_title"],
  );
}

WindowsAuthMessages? parseWindowsAuthMessages(Map? value) {
  if (value == null) {
    return null;
  }
  return const WindowsAuthMessages();
}

List<AuthMessages> parseAuthMessages(
  Map? args, {
  List<AuthMessages> defaults = const [
    IOSAuthMessages(),
    AndroidAuthMessages(),
    WindowsAuthMessages(),
  ],
}) {
  final android = parseAndroidAuthMessages(args?["android_messages"]);
  final ios = parseIosAuthMessages(args?["ios_messages"]);
  final windows = parseWindowsAuthMessages(args?["windows_messages"]);

  if (android == null && ios == null && windows == null) {
    return defaults;
  }

  final messages = <AuthMessages>[];
  for (final message in defaults) {
    if (message is AndroidAuthMessages) {
      messages.add(android ?? message);
    } else if (message is IOSAuthMessages) {
      messages.add(ios ?? message);
    } else if (message is WindowsAuthMessages) {
      messages.add(windows ?? message);
    } else {
      messages.add(message);
    }
  }
  return messages;
}

String? parseBiometricTypeName(BiometricType type) {
  return type.name;
}

LocalAuthExceptionCode parseLocalAuthExceptionCode(String? value) {
  return LocalAuthExceptionCode.values.firstWhere(
    (code) => code.name == value,
    orElse: () => LocalAuthExceptionCode.unknownError,
  );
}

Map<String, Object?> localAuthErrorMap(LocalAuthException exception) {
  return {
    "error_code": exception.code.name,
    "error_description": exception.description,
  };
}
