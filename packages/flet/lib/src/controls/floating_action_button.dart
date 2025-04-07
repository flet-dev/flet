import 'package:flet/src/utils/borders.dart';
import 'package:flet/src/utils/colors.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../widgets/error.dart';
import 'base_controls.dart';
import 'control_widget.dart';

class FloatingActionButtonControl extends StatelessWidget {
  final Control control;

  const FloatingActionButtonControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("FloatingActionButtonControl build: ${control.id}");

    String? text = control.getString("text"); //to be removed in 0.70.3
    var content = control.get("content");

    Widget? contentWidget = content is Control
        ? ControlWidget(control: content)
        : content is String
            ? Text(content)
            : text != null
                ? Text(text)
                : null;

    var icon = control.get("icon");
    var iconWidget = icon is Control
        ? ControlWidget(control: icon)
        : icon is String
            ? Icon(parseIcon(icon))
            : null;

    var url = control.getString("url", "")!;
    var urlTarget = control.getString("url_target");
    var disabledElevation = control.getDouble("disabled_elevation");
    var elevation = control.getDouble("elevation");
    var hoverElevation = control.getDouble("hover_elevation");
    var highlightElevation = control.getDouble("highlight_elevation");
    var focusElevation = control.getDouble("focus_elevation");
    var bgColor = control.getColor("bgcolor", context);
    var foregroundColor = control.getColor("foreground_color", context);
    var splashColor = control.getColor("splash_color", context);
    var hoverColor = control.getColor("hover_color", context);
    var focusColor = control.getColor("focus_color", context);
    var shape = control.getShape("shape");
    var clipBehavior =
        parseClip(control.getString("clip_behavior"), Clip.none)!;

    bool autofocus = control.getBool("autofocus", false)!;
    bool mini = control.getBool("mini", false)!;
    bool? enableFeedback = control.getBool("enable_feedback");
    var mouseCursor = control.getMouseCursor("mouse_cursor");

    Function()? onPressed = control.disabled
        ? null
        : () {
            if (url != "") {
              openWebBrowser(url, webWindowName: urlTarget);
            }
            FletBackend.of(context).triggerControlEvent(control, "click");
          };

    if (iconWidget == null && contentWidget == null) {
      return const ErrorControl(
          "FloatingActionButton has nothing to display. Provide at minimum one of these: text, icon, content"); //text to be removed in 0.70.3
    }
    var child = iconWidget != null
        ? contentWidget == null
            ? iconWidget
            : null
        : contentWidget;

    Widget button;
    if (child != null) {
      button = FloatingActionButton(
          heroTag: control.id,
          autofocus: autofocus,
          onPressed: onPressed,
          mouseCursor: mouseCursor,
          backgroundColor: bgColor,
          foregroundColor: foregroundColor,
          hoverColor: hoverColor,
          splashColor: splashColor,
          elevation: elevation,
          disabledElevation: disabledElevation,
          focusElevation: focusElevation,
          hoverElevation: hoverElevation,
          highlightElevation: highlightElevation,
          enableFeedback: enableFeedback,
          clipBehavior: clipBehavior,
          focusColor: focusColor,
          shape: shape,
          mini: mini,
          child: child);
    } else if (contentWidget != null) {
      button = FloatingActionButton.extended(
        heroTag: control.id,
        autofocus: autofocus,
        onPressed: onPressed,
        mouseCursor: mouseCursor,
        label: contentWidget,
        icon: iconWidget,
        backgroundColor: bgColor,
        foregroundColor: foregroundColor,
        hoverColor: hoverColor,
        splashColor: splashColor,
        elevation: elevation,
        disabledElevation: disabledElevation,
        focusElevation: focusElevation,
        hoverElevation: hoverElevation,
        highlightElevation: highlightElevation,
        enableFeedback: enableFeedback,
        clipBehavior: clipBehavior,
        focusColor: focusColor,
        shape: shape,
      );
    } else {
      return const ErrorControl(
          "FloatingActionButton has nothing to display. Provide at minimum one of these: text, icon, content");
    }

    return ConstrainedControl(control: control, child: button);
  }
}
