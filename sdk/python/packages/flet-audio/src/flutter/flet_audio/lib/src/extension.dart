import 'package:audioplayers/audioplayers.dart';
import 'package:flet/flet.dart';

import 'audio.dart';
import 'utils/audio.dart';

class Extension extends FletExtension {
  /// Makes the default `AudioContext` the one every new player starts with, so
  /// on Android each `Audio` plays alongside the others instead of pausing them.
  ///
  /// It is set here, before any player exists, so that an `Audio` without a
  /// `context` never has to apply one: applying a context to an Android player
  /// also overwrites the device's audio mode and speakerphone setting. Setting
  /// this default overwrites them too, but only here, as the app starts.
  ///
  /// Other platforms keep their default, as iOS already plays every `Audio` of
  /// an app together and only mobile platforms support audio contexts.
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
