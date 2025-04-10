import 'dart:convert';

import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class InteractiveViewerControl extends StatefulWidget {
  final Control control;

  const InteractiveViewerControl({super.key, required this.control});

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
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("OutlinedButton.$name($args)");
    switch (name) {
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
        var duration = parseDuration(args["duration"]);
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
      default:
        throw Exception("Unknown InteractiveViewer method: $name");
    }
  }

  @override
  void dispose() {
    _transformationController.dispose();
    _animationController.dispose();
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("InteractiveViewer build: ${widget.control.id}");

    var content = widget.control.buildWidget("content");
    var interactiveViewer = InteractiveViewer(
      transformationController: _transformationController,
      panEnabled: widget.control.getBool("pan_enabled", true)!,
      scaleEnabled: widget.control.getBool("scale_enabled", true)!,
      trackpadScrollCausesScale:
          widget.control.getBool("trackpad_scroll_causes_scale", false)!,
      constrained: widget.control.getBool("constrained", true)!,
      maxScale: widget.control.getDouble("max_scale", 2.5)!,
      minScale: widget.control.getDouble("min_scale", 0.8)!,
      interactionEndFrictionCoefficient: widget.control
          .getDouble("interaction_end_friction_coefficient", 0.0000135)!,
      scaleFactor: widget.control.getDouble("scale_factor", 200)!,
      clipBehavior:
          parseClip(widget.control.getString("clip_behavior"), Clip.hardEdge)!,
      alignment: widget.control.get("alignment"),
      boundaryMargin:
          widget.control.getMargin("boundary_margin", EdgeInsets.zero)!,
      onInteractionStart: !widget.control.disabled
          ? (ScaleStartDetails details) {
              widget.control.triggerEvent("interaction_start", {
                "pc": details.pointerCount,
                "gfp": {"x": details.focalPoint.dx, "y": details.focalPoint.dy},
                "lfp": {
                  "x": details.localFocalPoint.dx,
                  "y": details.localFocalPoint.dy
                },
              });
            }
          : null,
      onInteractionEnd: !widget.control.disabled
          ? (ScaleEndDetails details) {
              widget.control.triggerEvent(
                  "interaction_end",
                  jsonEncode({
                    "pc": details.pointerCount,
                    "sv": details.scaleVelocity,
                  }));
            }
          : null,
      onInteractionUpdate: !widget.control.disabled
          ? (ScaleUpdateDetails details) {
              var interactionUpdateInterval =
                  widget.control.getInt("interactionUpdateInterval", 200)!;
              var now = DateTime.now().millisecondsSinceEpoch;
              if (now - _interactionUpdateTimestamp >
                  interactionUpdateInterval) {
                _interactionUpdateTimestamp = now;
                widget.control.triggerEvent("interaction_update", {
                  "pc": details.pointerCount,
                  "fp_x": details.focalPoint.dx,
                  "fp_y": details.focalPoint.dy,
                  "lfp_x": details.localFocalPoint.dx,
                  "lfp_y": details.localFocalPoint.dy,
                  "s": details.scale,
                  "hs": details.horizontalScale,
                  "vs": details.verticalScale,
                  "rot": details.rotation,
                });
              }
            }
          : null,
      child: content ??
          const ErrorControl(
              "InteractiveViewer.content must be provided and visible"),
    );

    return ConstrainedControl(
        control: widget.control, child: interactiveViewer);
  }
}
