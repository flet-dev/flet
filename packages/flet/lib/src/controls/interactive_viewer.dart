import 'package:flet/src/utils/events.dart';
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

  InteractiveViewerControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

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
    debugPrint("InteractiveViewer.$name($args)");
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
        if (dx != null) {
          _transformationController.value =
              _transformationController.value.clone()
                ..translate(
                  dx,
                  parseDouble(args["dy"], 0)!,
                  parseDouble(args["dz"], 0)!,
                );
        }
        break;
      case "reset":
        var animationDuration = parseDuration(args["animation_duration"]);
        if (animationDuration == null) {
          _transformationController.value = Matrix4.identity();
        } else {
          _animationController.duration = animationDuration;
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
              widget.control.triggerEvent("interaction_start", details.toMap());
            }
          : null,
      onInteractionEnd: !widget.control.disabled
          ? (ScaleEndDetails details) {
              widget.control.triggerEvent("interaction_end", details.toMap());
            }
          : null,
      onInteractionUpdate: !widget.control.disabled
          ? (ScaleUpdateDetails details) {
              var interactionUpdateInterval =
                  widget.control.getInt("interaction_update_interval", 200)!;
              var now = DateTime.now().millisecondsSinceEpoch;
              if (now - _interactionUpdateTimestamp >
                  interactionUpdateInterval) {
                _interactionUpdateTimestamp = now;
                widget.control
                    .triggerEvent("interaction_update", details.toMap());
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
