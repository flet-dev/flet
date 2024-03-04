import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';

class CircleAvatarControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const CircleAvatarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("CircleAvatar build: ${control.id}");

    bool disabled = control.isDisabled || parentDisabled;
    var foregroundImageUrl = control.attrString("foregroundImageUrl");
    var backgroundImageUrl = control.attrString("backgroundImageUrl");
    var contentCtrls = children.where((c) => c.name == "content");

    var avatar = CircleAvatar(
        foregroundImage: foregroundImageUrl != null
            ? NetworkImage(foregroundImageUrl)
            : null,
        backgroundImage: backgroundImageUrl != null
            ? NetworkImage(backgroundImageUrl)
            : null,
        backgroundColor: HexColor.fromString(
            Theme.of(context), control.attrString("bgColor", "")!),
        foregroundColor: HexColor.fromString(
            Theme.of(context), control.attrString("color", "")!),
        radius: control.attrDouble("radius"),
        minRadius: control.attrDouble("minRadius"),
        maxRadius: control.attrDouble("maxRadius"),
        onBackgroundImageError: (object, trace) {
          backend.triggerControlEvent(control.id, "imageError");
        },
        onForegroundImageError: (object, trace) {
          backend.triggerControlEvent(control.id, "imageError");
        },
        child: contentCtrls.isNotEmpty
            ? createControl(control, contentCtrls.first.id, disabled)
            : null);

    return constrainedControl(context, avatar, parent, control);
  }
}
