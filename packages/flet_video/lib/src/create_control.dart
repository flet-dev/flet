import 'package:flet/flet.dart';
import 'package:media_kit/media_kit.dart';

import 'video.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "video":
      return VideoControl(
          parent: args.parent, control: args.control, backend: args.backend);
    default:
      return null;
  }
};

void ensureInitialized() {
  MediaKit.ensureInitialized();
}
