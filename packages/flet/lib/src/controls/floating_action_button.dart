import 'package:flet/src/flet_backend.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import '../utils/mouse.dart';
import '../utils/others.dart';
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
    Widget? iconWidget = icon is Control
        ? ControlWidget(control: icon)
        : icon is String
            ? Icon(parseIcon(icon))
            : null;

    String url = control.getString("url", "")!;
    String? urlTarget = control.getString("url_target");
    double? disabledElevation = control.getDouble("disabled_elevation");
    double? elevation = control.getDouble("elevation");
    double? hoverElevation = control.getDouble("hover_elevation");
    double? highlightElevation = control.getDouble("highlight_elevation");
    double? focusElevation = control.getDouble("focus_elevation");
    Color? bgColor = control.getColor("bgcolor", context);
    Color? foregroundColor = control.getColor("foreground_color", context);
    Color? splashColor = control.getColor("splash_color", context);
    Color? hoverColor = control.getColor("hover_color", context);
    Color? focusColor = control.getColor("focus_color", context);
    OutlinedBorder? shape = parseOutlinedBorder(control, "shape");
    var clipBehavior =
        parseClip(control.getString("clip_behavior"), Clip.none)!;

    bool autofocus = control.getBool("autofocus", false)!;
    bool mini = control.getBool("mini", false)!;
    bool? enableFeedback = control.getBool("enable_feedback");
    var mouseCursor = parseMouseCursor(control.getString("mouse_cursor"));
    bool disabled = control.disabled || control.parent!.disabled;

    Function()? onPressed = disabled
        ? null
        : () {
            debugPrint("FloatingActionButtonControl ${control.id} clicked!");
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
