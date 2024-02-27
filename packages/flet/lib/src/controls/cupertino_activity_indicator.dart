import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';

class CupertinoActivityIndicatorControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final FletControlBackend backend;

  const CupertinoActivityIndicatorControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.backend});

  @override
  State<CupertinoActivityIndicatorControl> createState() =>
      _CupertinoActivityIndicatorControlState();
}

class _CupertinoActivityIndicatorControlState
    extends State<CupertinoActivityIndicatorControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoActivityIndicatorControl build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    return constrainedControl(
        context,
        CupertinoActivityIndicator(
          radius: widget.control.attrDouble("radius", 10)!,
          animating: widget.control.attrBool("animating", true)!,
          color: HexColor.fromString(
              Theme.of(context), widget.control.attrString("color", "")!),
        ),
        widget.parent,
        widget.control);
  }
}
