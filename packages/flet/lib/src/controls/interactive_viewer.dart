import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
import 'create_control.dart';
import 'error.dart';

class InteractiveViewerControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const InteractiveViewerControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("InteractiveViewer build: ${control.id}");

    var contentCtrls = children.where((c) => c.isVisible);
    bool? adaptive = control.attrBool("adaptive") ?? parentAdaptive;
    bool disabled = control.isDisabled || parentDisabled;

    var interactiveViewer = InteractiveViewer(
      panEnabled: control.attrBool("panEnabled", true)!,
      scaleEnabled: control.attrBool("scaleEnabled", true)!,
      trackpadScrollCausesScale:
          control.attrBool("trackpadScrollCausesScale", false)!,
      constrained: control.attrBool("constrained", true)!,
      maxScale: control.attrDouble("maxScale", 2.5)!,
      minScale: control.attrDouble("minScale", 0.8)!,
      interactionEndFrictionCoefficient:
          control.attrDouble("interactionEndFrictionCoefficient", 0.0000135)!,
      scaleFactor: control.attrDouble("scaleFactor", 200)!,
      clipBehavior:
          parseClip(control.attrString("clipBehavior"), Clip.hardEdge)!,
      alignment: parseAlignment(control, "alignment"),
      boundaryMargin:
          parseEdgeInsets(control, "boundaryMargin", EdgeInsets.zero)!,
      onInteractionStart: !disabled
          ? (ScaleStartDetails details) {
              debugPrint("InteractiveViewer ${control.id} onInteractionStart");
              backend.triggerControlEvent(
                  control.id,
                  "interaction_start",
                  jsonEncode({
                    "pc": details.pointerCount,
                    "fp_x": details.focalPoint.dx,
                    "fp_y": details.focalPoint.dy,
                    "lfp_x": details.localFocalPoint.dx,
                    "lfp_y": details.localFocalPoint.dy
                  }));
            }
          : null,
      onInteractionEnd: !disabled
          ? (ScaleEndDetails details) {
              debugPrint("InteractiveViewer ${control.id} onInteractionEnd");
              backend.triggerControlEvent(
                  control.id,
                  "interaction_end",
                  jsonEncode({
                    "pc": details.pointerCount,
                    "sv": details.scaleVelocity,
                  }));
            }
          : null,
      onInteractionUpdate: !disabled
          ? (ScaleUpdateDetails details) {
              debugPrint("InteractiveViewer ${control.id} onInteractionUpdate");
              backend.triggerControlEvent(
                  control.id,
                  "interaction_update",
                  jsonEncode({
                    "pc": details.pointerCount,
                    "fp_x": details.focalPoint.dx,
                    "fp_y": details.focalPoint.dy,
                    "lfp_x": details.localFocalPoint.dx,
                    "lfp_y": details.localFocalPoint.dy,
                    "s": details.scale,
                    "hs": details.horizontalScale,
                    "vs": details.verticalScale,
                    "rot": details.rotation,
                  }));
            }
          : null,
      child: contentCtrls.isNotEmpty
          ? createControl(control, contentCtrls.first.id, disabled,
              parentAdaptive: adaptive)
          : const ErrorControl(
              "InteractiveViewer.content must be provided and visible"),
    );
    return constrainedControl(context, interactiveViewer, parent, control);
  }
}
