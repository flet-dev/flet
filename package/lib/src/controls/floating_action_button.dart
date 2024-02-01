import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import '../utils/transforms.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_control_stateless_mixin.dart';

class FloatingActionButtonControl extends StatelessWidget
    with FletControlStatelessMixin {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const FloatingActionButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("FloatingActionButtonControl build: ${control.id}");

    String? text = control.attrString("text");
    IconData? icon = parseIcon(control.attrString("icon", "")!);
    String url = control.attrString("url", "")!;
    String? urlTarget = control.attrString("urlTarget");
    Color? bgColor = HexColor.fromString(
        Theme.of(context), control.attrString("bgColor", "")!);
    OutlinedBorder? shape = parseOutlinedBorder(control, "shape");
    var contentCtrls = children.where((c) => c.name == "content");
    var tooltip = control.attrString("tooltip");
    bool autofocus = control.attrBool("autofocus", false)!;
    bool mini = control.attrBool("mini", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    Function()? onPressed = disabled
        ? null
        : () {
            debugPrint("FloatingActionButtonControl ${control.id} clicked!");
            if (url != "") {
              openWebBrowser(url, webWindowName: urlTarget);
            }
            sendControlEvent(context, control.id, "click", "");
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
          backgroundColor: bgColor,
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
          backgroundColor: bgColor,
          tooltip: tooltip,
          shape: shape,
          mini: mini,
          child: Icon(icon));
    } else if (icon == null && text != null) {
      button = FloatingActionButton(
        heroTag: control.id,
        autofocus: autofocus,
        onPressed: onPressed,
        backgroundColor: bgColor,
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
        label: Text(text),
        icon: Icon(icon),
        backgroundColor: bgColor,
        tooltip: tooltip,
        shape: shape,
      );
    } else {
      return const ErrorControl("FAB doesn't have a text, nor icon.");
    }

    return constrainedControl(context, button, parent, control);
  }
}

FloatingActionButtonLocation parseFloatingActionButtonLocation(
    Control control, String propName, FloatingActionButtonLocation defValue) {
  List<FloatingActionButtonLocation> fabLocations = [
    FloatingActionButtonLocation.centerDocked,
    FloatingActionButtonLocation.centerFloat,
    FloatingActionButtonLocation.centerTop,
    FloatingActionButtonLocation.endContained,
    FloatingActionButtonLocation.endDocked,
    FloatingActionButtonLocation.endFloat,
    FloatingActionButtonLocation.endTop,
    FloatingActionButtonLocation.miniCenterDocked,
    FloatingActionButtonLocation.miniCenterFloat,
    FloatingActionButtonLocation.miniCenterTop,
    FloatingActionButtonLocation.miniEndFloat,
    FloatingActionButtonLocation.miniEndTop,
    FloatingActionButtonLocation.miniStartDocked,
    FloatingActionButtonLocation.miniStartFloat,
    FloatingActionButtonLocation.miniStartTop,
    FloatingActionButtonLocation.startDocked,
    FloatingActionButtonLocation.startFloat,
    FloatingActionButtonLocation.startTop
  ];

  try {
    OffsetDetails? fabLocationOffsetDetails = parseOffset(control, propName);
    if (fabLocationOffsetDetails != null) {
      return CustomFloatingActionButtonLocation(
          dx: fabLocationOffsetDetails.x, dy: fabLocationOffsetDetails.y);
    } else {
      return defValue;
    }
  } catch (e) {
    return fabLocations.firstWhere(
        (l) =>
            l.toString().split('.').last.toLowerCase() ==
            control.attrString(propName, "")!.toLowerCase(),
        orElse: () => defValue);
  }
}

class CustomFloatingActionButtonLocation extends FloatingActionButtonLocation {
  final double dx;
  final double dy;

  CustomFloatingActionButtonLocation({required this.dx, required this.dy});

  @override
  Offset getOffset(ScaffoldPrelayoutGeometry scaffoldGeometry) {
    return Offset(scaffoldGeometry.scaffoldSize.width - dx,
        scaffoldGeometry.scaffoldSize.height - dy);
  }

  @override
  bool operator ==(Object other) =>
      other is CustomFloatingActionButtonLocation &&
      other.dx == dx &&
      other.dy == dy;

  @override
  int get hashCode => dx.hashCode + dy.hashCode;

  @override
  String toString() => 'CustomFloatingActionButtonLocation';
}
