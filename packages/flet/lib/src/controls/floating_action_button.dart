import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import '../utils/mouse.dart';
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

    String? text = control.attrString("text");
    IconData? icon = parseIcon(control.attrString("icon", "")!);
    String url = control.attrString("url", "")!;
    String? urlTarget = control.attrString("urlTarget");
    double? disabledElevation = control.attrDouble("disabledElevation");
    double? elevation = control.attrDouble("elevation");
    double? hoverElevation = control.attrDouble("hoverElevation");
    double? highlightElevation = control.attrDouble("highlightElevation");
    double? focusElevation = control.attrDouble("focusElevation");
    Color? bgColor = control.attrColor("bgColor", context);
    Color? foregroundColor = control.attrColor("foregroundColor", context);
    Color? splashColor = control.attrColor("splashColor", context);
    Color? hoverColor = control.attrColor("hoverColor", context);
    Color? focusColor = control.attrColor("focusColor", context);
    OutlinedBorder? shape = parseOutlinedBorder(control, "shape");
    var clipBehavior = Clip.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("clipBehavior", "")!.toLowerCase(),
        orElse: () => Clip.none);
    var contentCtrls = children.where((c) => c.name == "content");
    var tooltip = control.attrString("tooltip");
    bool autofocus = control.attrBool("autofocus", false)!;
    bool mini = control.attrBool("mini", false)!;
    bool? enableFeedback = control.attrBool("enableFeedback");
    bool disabled = control.isDisabled || parentDisabled;

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
          "FAB doesn't have a text, nor icon, nor content.");
    }

    Widget button;
    if (contentCtrls.isNotEmpty) {
      button = FloatingActionButton(
          heroTag: control.id,
          autofocus: autofocus,
          onPressed: onPressed,
          mouseCursor: parseMouseCursor(control.attrString("mouseCursor")),
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
          tooltip: tooltip,
          shape: shape,
          mini: mini,
          child: createControl(control, contentCtrls.first.id, disabled,
              parentAdaptive: parentAdaptive));
    } else if (icon != null && text == null) {
      button = FloatingActionButton(
          heroTag: control.id,
          autofocus: autofocus,
          onPressed: onPressed,
          mouseCursor: parseMouseCursor(control.attrString("mouseCursor")),
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
          tooltip: tooltip,
          shape: shape,
          mini: mini,
          child: Icon(icon));
    } else if (icon == null && text != null) {
      button = FloatingActionButton(
        heroTag: control.id,
        autofocus: autofocus,
        onPressed: onPressed,
        mouseCursor: parseMouseCursor(control.attrString("mouseCursor")),
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
        tooltip: tooltip,
        shape: shape,
        mini: mini,
        child: Text(text),
      );
    } else if (icon != null && text != null) {
      button = FloatingActionButton.extended(
        heroTag: control.id,
        autofocus: autofocus,
        onPressed: onPressed,
        mouseCursor: parseMouseCursor(control.attrString("mouseCursor")),
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
        tooltip: tooltip,
        shape: shape,
      );
    } else {
      return const ErrorControl("FAB doesn't have a text, nor icon.");
    }

    return constrainedControl(context, button, parent, control);
  }
}
