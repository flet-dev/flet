import 'package:flet/flet.dart';
import 'package:flutter/cupertino.dart';
import 'package:media_kit/media_kit.dart';

import 'video.dart';

class Extension extends FletExtension {
  @override
  void ensureInitialized() {
    MediaKit.ensureInitialized();
  }

  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "Video":
        return VideoControl(key: key, control: control);
      default:
        return null;
    }
  }
}
