import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'hello_world_control.dart';

Map<String, Widget Function(Control?, ControlViewModel)> controlsMapping = {
  "helloworld": (parent, controlView) =>
      HelloWorldControl(parent: parent, control: controlView.control),
};
