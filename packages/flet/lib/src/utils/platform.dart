import 'package:flutter/foundation.dart';

/// Checks if the current platform is a desktop platform.
bool isDesktopPlatform() {
  return !kIsWeb &&
      (defaultTargetPlatform == TargetPlatform.windows ||
          defaultTargetPlatform == TargetPlatform.macOS ||
          defaultTargetPlatform == TargetPlatform.linux);
}

/// Checks if the current platform is a mobile (iOS or Android) platform.
bool isMobilePlatform() {
  return !kIsWeb &&
      (defaultTargetPlatform == TargetPlatform.iOS ||
          defaultTargetPlatform == TargetPlatform.android);
}

/// Checks if the current platform is Windows desktop.
bool isWindowsDesktop() {
  return !kIsWeb && (defaultTargetPlatform == TargetPlatform.windows);
}

/// Checks if the current platform is macOS desktop.
bool isMacOSDesktop() {
  return !kIsWeb && (defaultTargetPlatform == TargetPlatform.macOS);
}

/// Checks if the current platform is Linux desktop.
bool isLinuxDesktop() {
  return !kIsWeb && (defaultTargetPlatform == TargetPlatform.linux);
}

/// Checks if the current platform is a web platform.
bool isWebPlatform() {
  return kIsWeb == true;
}
