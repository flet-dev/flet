import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/launch_url.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class FloatingActionButtonControl extends StatelessWidget {
  final Control control;

  const FloatingActionButtonControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("FloatingActionButtonControl build: ${control.id}");

    var content = control.buildTextOrWidget("content");
    var icon = control.buildIconOrWidget("icon");
    var url = control.getUrl("url");
    var disabledElevation = control.getDouble("disabled_elevation");
    var elevation = control.getDouble("elevation");
    var hoverElevation = control.getDouble("hover_elevation");
    var highlightElevation = control.getDouble("highlight_elevation");
    var focusElevation = control.getDouble("focus_elevation");
    var bgcolor = control.getColor("bgcolor", context);
    var foregroundColor = control.getColor("foreground_color", context);
    var splashColor = control.getColor("splash_color", context);
    var hoverColor = control.getColor("hover_color", context);
    var focusColor = control.getColor("focus_color", context);
    var shape = control.getShape("shape", Theme.of(context));
    var clipBehavior =
        parseClip(control.getString("clip_behavior"), Clip.none)!;
    var autofocus = control.getBool("autofocus", false)!;
    var mini = control.getBool("mini", false)!;
    var enableFeedback = control.getBool("enable_feedback");
    var mouseCursor = control.getMouseCursor("mouse_cursor");

    Function()? onPressed = control.disabled
        ? null
        : () {
            if (url != null) {
              openWebBrowser(url);
            }
            control.triggerEvent("click");
          };

    if (icon == null && content == null) {
      return const ErrorControl(
          "FloatingActionButton has nothing to display. Provide at minimum one of these: icon, content");
    }
    var child = icon != null
        ? content == null
            ? icon
            : null
        : content;

    Widget button;
    if (child != null) {
      button = FloatingActionButton(
          heroTag: control.id,
          autofocus: autofocus,
          onPressed: onPressed,
          mouseCursor: mouseCursor,
          backgroundColor: bgcolor,
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
    } else if (content != null) {
      button = FloatingActionButton.extended(
        heroTag: control.id,
        autofocus: autofocus,
        onPressed: onPressed,
        mouseCursor: mouseCursor,
        label: content,
        icon: icon,
        backgroundColor: bgcolor,
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
          "FloatingActionButton has nothing to display. Provide at minimum icon or content.");
    }

    return ConstrainedControl(control: control, child: button);
  }
}
