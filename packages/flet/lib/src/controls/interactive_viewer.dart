import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../utils/others.dart';
import '../utils/time.dart';
import 'create_control.dart';
import 'error.dart';

class InteractiveViewerControl extends StatefulWidget {
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
  State<InteractiveViewerControl> createState() =>
      _InteractiveViewerControlState();
}

class _InteractiveViewerControlState extends State<InteractiveViewerControl>
    with SingleTickerProviderStateMixin {
  final TransformationController _transformationController =
      TransformationController();
  late AnimationController _animationController;
  Animation<Matrix4>? _animation;
  Matrix4? _savedMatrix;
  int _interactionUpdateTimestamp = DateTime.now().millisecondsSinceEpoch;

  @override
  void initState() {
    super.initState();
    _animationController =
        AnimationController(vsync: this, duration: Duration.zero);

    widget.backend.subscribeMethods(widget.control.id,
        (methodName, args) async {
      switch (methodName) {
        case "zoom":
          var factor = parseDouble(args["factor"]);
          if (factor != null) {
            _transformationController.value =
                _transformationController.value.scaled(factor, factor);
          }
          break;
        case "pan":
          var dx = parseDouble(args["dx"]);
          var dy = parseDouble(args["dy"]);
          if (dx != null && dy != null) {
            _transformationController.value =
                _transformationController.value.clone()..translate(dx, dy);
          }
          break;
        case "reset":
          var duration = durationFromString(args["duration"]);
          if (duration == null) {
            _transformationController.value = Matrix4.identity();
          } else {
            _animationController.duration = duration;
            _animation = Matrix4Tween(
              begin: _transformationController.value,
              end: Matrix4.identity(),
            ).animate(_animationController)
              ..addListener(() {
                _transformationController.value = _animation!.value;
              });
            _animationController.forward(from: 0);
          }
          break;
        case "save_state":
          _savedMatrix = _transformationController.value.clone();
          break;
        case "restore_state":
          if (_savedMatrix != null) {
            _transformationController.value = _savedMatrix!;
          }
          break;
      }
      return null;
    });
  }

  @override
  void dispose() {
    _transformationController.dispose();
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("InteractiveViewer build: ${widget.control.id}");

    var contentCtrls = widget.children.where((c) => c.isVisible);
    bool? adaptive = widget.control.isAdaptive ?? widget.parentAdaptive;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var interactiveViewer = InteractiveViewer(
      transformationController: _transformationController,
      panEnabled: widget.control.attrBool("panEnabled", true)!,
      scaleEnabled: widget.control.attrBool("scaleEnabled", true)!,
      trackpadScrollCausesScale:
          widget.control.attrBool("trackpadScrollCausesScale", false)!,
      constrained: widget.control.attrBool("constrained", true)!,
      maxScale: widget.control.attrDouble("maxScale", 2.5)!,
      minScale: widget.control.attrDouble("minScale", 0.8)!,
      interactionEndFrictionCoefficient: widget.control
          .attrDouble("interactionEndFrictionCoefficient", 0.0000135)!,
      scaleFactor: widget.control.attrDouble("scaleFactor", 200)!,
      clipBehavior:
          parseClip(widget.control.attrString("clipBehavior"), Clip.hardEdge)!,
      alignment: parseAlignment(widget.control, "alignment"),
      boundaryMargin:
          parseEdgeInsets(widget.control, "boundaryMargin", EdgeInsets.zero)!,
      onInteractionStart: !disabled
          ? (ScaleStartDetails details) {
              debugPrint(
                  "InteractiveViewer ${widget.control.id} onInteractionStart");
              widget.backend.triggerControlEvent(
                  widget.control.id,
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
              debugPrint(
                  "InteractiveViewer ${widget.control.id} onInteractionEnd");
              widget.backend.triggerControlEvent(
                  widget.control.id,
                  "interaction_end",
                  jsonEncode({
                    "pc": details.pointerCount,
                    "sv": details.scaleVelocity,
                  }));
            }
          : null,
      onInteractionUpdate: !disabled
          ? (ScaleUpdateDetails details) {
              var interactionUpdateInterval =
                  widget.control.attrInt("interactionUpdateInterval", 200)!;
              var now = DateTime.now().millisecondsSinceEpoch;
              if (now - _interactionUpdateTimestamp >
                  interactionUpdateInterval) {
                debugPrint(
                    "InteractiveViewer ${widget.control.id} onInteractionUpdate");
                _interactionUpdateTimestamp = now;
                widget.backend.triggerControlEvent(
                    widget.control.id,
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
                ;
              }
            }
          : null,
      child: contentCtrls.isNotEmpty
          ? createControl(widget.control, contentCtrls.first.id, disabled,
              parentAdaptive: adaptive)
          : const ErrorControl(
              "InteractiveViewer.content must be provided and visible"),
    );

    return constrainedControl(
        context, interactiveViewer, widget.parent, widget.control);
  }
}
