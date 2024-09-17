import 'package:flutter/foundation.dart';

bool isDesktop() {
  return !kIsWeb &&
      (defaultTargetPlatform == TargetPlatform.windows ||
          defaultTargetPlatform == TargetPlatform.macOS ||
          defaultTargetPlatform == TargetPlatform.linux);
}

bool isMobile() {
  return !kIsWeb &&
      (defaultTargetPlatform == TargetPlatform.iOS ||
          defaultTargetPlatform == TargetPlatform.android);
}

bool isWindowsDesktop() {
  return !kIsWeb && (defaultTargetPlatform == TargetPlatform.windows);
}

bool isWeb() {
  return kIsWeb == true;
}
