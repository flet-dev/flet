import 'dart:math' as math;

import 'package:flet/src/utils/events.dart';
import 'package:flutter/foundation.dart' show clampDouble;
import 'package:flutter/material.dart';
import 'package:vector_math/vector_math_64.dart' show Matrix4, Quad, Vector3;

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
  final GlobalKey _childKey = GlobalKey();
  late AnimationController _animationController;
  Animation<Matrix4>? _animation;
  Matrix4? _savedMatrix;
  int _interactionUpdateTimestamp = DateTime.now().millisecondsSinceEpoch;
  final double _currentRotation = 0.0;

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
              _matrixScale(_transformationController.value, factor);
        }
        break;
      case "pan":
        var dx = parseDouble(args["dx"]);
        if (dx != null) {
          final double dy = parseDouble(args["dy"], 0)!;
          final double dz = parseDouble(args["dz"], 0)!;
          final Matrix4 updated =
              _matrixTranslate(_transformationController.value, Offset(dx, dy));
          if (dz != 0) {
            updated.translateByDouble(0.0, 0.0, dz, 1.0);
          }
          _transformationController.value = updated;
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
    if (content == null) {
      return const ErrorControl(
          "InteractiveViewer.content must be provided and visible");
    }

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
      child: KeyedSubtree(key: _childKey, child: content),
    );

    return LayoutControl(control: widget.control, child: interactiveViewer);
  }

  Matrix4 _matrixScale(Matrix4 matrix, double scale) {
    if (scale == 1.0) {
      return matrix.clone();
    }

    final double currentScale = matrix.getMaxScaleOnAxis();
    if (currentScale == 0) {
      return matrix.clone();
    }

    final double minScale = widget.control.getDouble("min_scale", 0.8)!;
    final double maxScale = widget.control.getDouble("max_scale", 2.5)!;
    double totalScale = currentScale * scale;

    final Rect? boundaryRect = _currentBoundaryRect();
    final Rect? viewportRect = _currentViewportRect();
    if (boundaryRect != null &&
        viewportRect != null &&
        boundaryRect.width > 0 &&
        boundaryRect.height > 0 &&
        boundaryRect.width.isFinite &&
        boundaryRect.height.isFinite &&
        viewportRect.width.isFinite &&
        viewportRect.height.isFinite) {
      final double minFitScale = math.max(
        viewportRect.width / boundaryRect.width,
        viewportRect.height / boundaryRect.height,
      );
      if (minFitScale.isFinite && minFitScale > 0) {
        totalScale = math.max(totalScale, minFitScale);
      }
    }

    final double clampedTotalScale =
        clampDouble(totalScale, minScale, maxScale);
    final double clampedScale = clampedTotalScale / currentScale;
    return matrix.clone()..scale(clampedScale, clampedScale, clampedScale);
  }

  Matrix4 _matrixTranslate(Matrix4 matrix, Offset translation) {
    if (translation == Offset.zero) {
      return matrix.clone();
    }

    final Matrix4 nextMatrix = matrix.clone()
      ..translate(translation.dx, translation.dy, 0);

    final Rect? boundaryRect = _currentBoundaryRect();
    final Rect? viewportRect = _currentViewportRect();
    if (boundaryRect == null || viewportRect == null) {
      return nextMatrix;
    }

    if (boundaryRect.isInfinite) {
      return nextMatrix;
    }

    final Quad nextViewport = _transformViewport(nextMatrix, viewportRect);
    final Quad boundsQuad =
        _axisAlignedBoundingBoxWithRotation(boundaryRect, _currentRotation);
    final Offset offendingDistance = _exceedsBy(boundsQuad, nextViewport);
    if (offendingDistance == Offset.zero) {
      return nextMatrix;
    }

    final Offset nextTotalTranslation = _getMatrixTranslation(nextMatrix);
    final double currentScale = matrix.getMaxScaleOnAxis();
    if (currentScale == 0) {
      return matrix.clone();
    }
    final Offset correctedTotalTranslation = Offset(
      nextTotalTranslation.dx - offendingDistance.dx * currentScale,
      nextTotalTranslation.dy - offendingDistance.dy * currentScale,
    );

    final Matrix4 correctedMatrix = matrix.clone()
      ..setTranslation(Vector3(
        correctedTotalTranslation.dx,
        correctedTotalTranslation.dy,
        0.0,
      ));

    final Quad correctedViewport =
        _transformViewport(correctedMatrix, viewportRect);
    final Offset offendingCorrectedDistance =
        _exceedsBy(boundsQuad, correctedViewport);
    if (offendingCorrectedDistance == Offset.zero) {
      return correctedMatrix;
    }

    if (offendingCorrectedDistance.dx != 0.0 &&
        offendingCorrectedDistance.dy != 0.0) {
      return matrix.clone();
    }

    final Offset unidirectionalCorrectedTotalTranslation = Offset(
      offendingCorrectedDistance.dx == 0.0 ? correctedTotalTranslation.dx : 0.0,
      offendingCorrectedDistance.dy == 0.0 ? correctedTotalTranslation.dy : 0.0,
    );

    return matrix.clone()
      ..setTranslation(Vector3(
        unidirectionalCorrectedTotalTranslation.dx,
        unidirectionalCorrectedTotalTranslation.dy,
        0.0,
      ));
  }

  Rect? _currentBoundaryRect() {
    final BuildContext? childContext = _childKey.currentContext;
    if (childContext == null) {
      return null;
    }
    final RenderObject? renderObject = childContext.findRenderObject();
    if (renderObject is! RenderBox) {
      return null;
    }
    final Size childSize = renderObject.size;
    final EdgeInsets boundaryMargin =
        widget.control.getMargin("boundary_margin", EdgeInsets.zero)!;
    return boundaryMargin.inflateRect(Offset.zero & childSize);
  }

  Rect? _currentViewportRect() {
    final RenderObject? renderObject = context.findRenderObject();
    if (renderObject is! RenderBox) {
      return null;
    }
    final Size size = renderObject.size;
    return Offset.zero & size;
  }

  Offset _getMatrixTranslation(Matrix4 matrix) {
    final Vector3 translation = matrix.getTranslation();
    return Offset(translation.x, translation.y);
  }

  Quad _transformViewport(Matrix4 matrix, Rect viewport) {
    final Matrix4 inverseMatrix = matrix.clone()..invert();
    return Quad.points(
      inverseMatrix.transform3(
        Vector3(viewport.topLeft.dx, viewport.topLeft.dy, 0.0),
      ),
      inverseMatrix.transform3(
        Vector3(viewport.topRight.dx, viewport.topRight.dy, 0.0),
      ),
      inverseMatrix.transform3(
        Vector3(viewport.bottomRight.dx, viewport.bottomRight.dy, 0.0),
      ),
      inverseMatrix.transform3(
        Vector3(viewport.bottomLeft.dx, viewport.bottomLeft.dy, 0.0),
      ),
    );
  }

  Quad _axisAlignedBoundingBoxWithRotation(Rect rect, double rotation) {
    final Matrix4 rotationMatrix = Matrix4.identity()
      ..translate(rect.size.width / 2, rect.size.height / 2, 0)
      ..rotateZ(rotation)
      ..translate(-rect.size.width / 2, -rect.size.height / 2, 0);
    final Quad boundariesRotated = Quad.points(
      rotationMatrix.transform3(Vector3(rect.left, rect.top, 0.0)),
      rotationMatrix.transform3(Vector3(rect.right, rect.top, 0.0)),
      rotationMatrix.transform3(Vector3(rect.right, rect.bottom, 0.0)),
      rotationMatrix.transform3(Vector3(rect.left, rect.bottom, 0.0)),
    );
    return InteractiveViewer.getAxisAlignedBoundingBox(boundariesRotated);
  }

  Offset _exceedsBy(Quad boundary, Quad viewport) {
    final List<Vector3> viewportPoints = <Vector3>[
      viewport.point0,
      viewport.point1,
      viewport.point2,
      viewport.point3,
    ];
    Offset largestExcess = Offset.zero;
    for (final Vector3 point in viewportPoints) {
      final Vector3 pointInside =
          InteractiveViewer.getNearestPointInside(point, boundary);
      final Offset excess =
          Offset(pointInside.x - point.x, pointInside.y - point.y);
      if (excess.dx.abs() > largestExcess.dx.abs()) {
        largestExcess = Offset(excess.dx, largestExcess.dy);
      }
      if (excess.dy.abs() > largestExcess.dy.abs()) {
        largestExcess = Offset(largestExcess.dx, excess.dy);
      }
    }

    return _roundOffset(largestExcess);
  }

  Offset _roundOffset(Offset offset) {
    return Offset(
      double.parse(offset.dx.toStringAsFixed(9)),
      double.parse(offset.dy.toStringAsFixed(9)),
    );
  }
}
