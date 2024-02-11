import 'package:flet/flet.dart';

import 'audio_recorder.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "audiorecorder":
      return AudioRecorderControl(
          parent: args.parent, control: args.control, backend: args.backend);
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to do
}
