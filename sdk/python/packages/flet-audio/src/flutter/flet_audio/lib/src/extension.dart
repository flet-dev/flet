import 'package:audioplayers/audioplayers.dart';
import 'package:flet/flet.dart';

import 'audio.dart';
import 'utils/audio.dart';

class Extension extends FletExtension {
  /// Makes the default `AudioContext` the one every new player starts with.
  ///
  /// Applying a context to a single Android player also overwrites the device's
  /// audio mode and speakerphone setting, so an `Audio` that doesn't set a context
  /// must not need one applied.
  @override
  void ensureInitialized() {
    if (isAndroidMobile()) {
      AudioPlayer.global.setAudioContext(parseAudioContext(null));
    }
  }

  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "Audio":
        return AudioService(control: control);
      default:
        return null;
    }
  }
}
