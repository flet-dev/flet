import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import '../utils/mouse.dart';
import '../utils/others.dart';
import 'create_control.dart';
import 'error.dart';

class FloatingActionButtonControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const FloatingActionButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("FloatingActionButtonControl build: ${control.id}");

    String? text = control.getString("text");
    IconData? icon = parseIcon(control.getString("icon"));
    String url = control.getString("url", "")!;
    String? urlTarget = control.getString("urlTarget");
    double? disabledElevation = control.getDouble("disabledElevation");
    double? elevation = control.getDouble("elevation");
    double? hoverElevation = control.getDouble("hoverElevation");
    double? highlightElevation = control.getDouble("highlightElevation");
    double? focusElevation = control.getDouble("focusElevation");
    Color? bgColor = control.getColor("bgColor", context);
    Color? foregroundColor = control.getColor("foregroundColor", context);
    Color? splashColor = control.getColor("splashColor", context);
    Color? hoverColor = control.getColor("hoverColor", context);
    Color? focusColor = control.getColor("focusColor", context);
    OutlinedBorder? shape = parseOutlinedBorder(control, "shape");
    var clipBehavior = parseClip(control.getString("clipBehavior"), Clip.none)!;
    var contentCtrls = children.where((c) => c.name == "content" && c.visible);
    bool autofocus = control.getBool("autofocus", false)!;
    bool mini = control.getBool("mini", false)!;
    bool? enableFeedback = control.getBool("enableFeedback");
    var mouseCursor = parseMouseCursor(control.getString("mouseCursor"));
    bool disabled = control.disabled || parentDisabled;

    Function()? onPressed = disabled
        ? null
        : () {
            debugPrint("FloatingActionButtonControl ${control.id} clicked!");
            if (url != "") {
              openWebBrowser(url, webWindowName: urlTarget);
            }
            backend.triggerControlEvent(control.id, "click");
          };

    if (text == null && icon == null && contentCtrls.isEmpty) {
      return const ErrorControl(
          "FloatingActionButton has nothing to display. Provide at minimum one of these: text, icon, content");
    }

    Widget button;
    if (contentCtrls.isNotEmpty) {
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
          child: createControl(control, contentCtrls.first.id, disabled,
              parentAdaptive: parentAdaptive));
    } else if (icon != null && text == null) {
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
          child: Icon(icon));
    } else if (icon == null && text != null) {
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
        child: Text(text),
      );
    } else if (icon != null && text != null) {
      button = FloatingActionButton.extended(
        heroTag: control.id,
        autofocus: autofocus,
        onPressed: onPressed,
        mouseCursor: mouseCursor,
        label: Text(text),
        icon: Icon(icon),
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

    return constrainedControl(context, button, parent, control);
  }
}
