import 'package:flet/flet.dart';

import 'audio_recorder.dart';

class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "AudioRecorder":
        return AudioRecorderService(control: control);
      default:
        return null;
    }
  }
}
