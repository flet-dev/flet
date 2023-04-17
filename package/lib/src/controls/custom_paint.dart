import 'dart:convert';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/custom_paint_draw_shape_view_model.dart';
import '../models/custom_paint_view_model.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/drawing.dart';
import '../utils/transforms.dart';
import 'create_control.dart';

typedef CustomPaintControlOnPaintCallback = void Function(Size size);

class CustomPaintControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const CustomPaintControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<CustomPaintControl> createState() => _CustomPaintControlState();
}

class _CustomPaintControlState extends State<CustomPaintControl> {
  int _lastResize = DateTime.now().millisecondsSinceEpoch;
  Size? _lastSize;

  @override
  Widget build(BuildContext context) {
    debugPrint("CustomPaint build: ${widget.control.id}");

    var result = StoreConnector<AppState, CustomPaintViewModel>(
        distinct: true,
        converter: (store) => CustomPaintViewModel.fromStore(
            store, widget.control, widget.children),
        builder: (context, viewModel) {
          var onResize = viewModel.control.attrBool("onResize", false)!;
          var resizeInterval = viewModel.control.attrInt("resizeInterval", 10)!;

          var paint = CustomPaint(
            painter: FletCustomPainter(
              theme: Theme.of(context),
              shapes: viewModel.shapes,
              onPaintCallback: (size) {
                if (onResize) {
                  var now = DateTime.now().millisecondsSinceEpoch;
                  if ((now - _lastResize > resizeInterval &&
                          _lastSize != size) ||
                      _lastSize == null) {
                    _lastResize = now;
                    _lastSize = size;
                    FletAppServices.of(context).server.sendPageEvent(
                        eventTarget: viewModel.control.id,
                        eventName: "resize",
                        eventData:
                            json.encode({"w": size.width, "h": size.height}));
                  }
                }
              },
            ),
          );

          return paint;
        });

    return constrainedControl(context, result, widget.parent, widget.control);
  }
}

class FletCustomPainter extends CustomPainter {
  final ThemeData theme;
  final List<CustomPaintDrawShapeViewModel> shapes;
  final CustomPaintControlOnPaintCallback onPaintCallback;

  const FletCustomPainter(
      {required this.theme,
      required this.shapes,
      required this.onPaintCallback});

  @override
  void paint(Canvas canvas, Size size) {
    onPaintCallback(size);

    //debugPrint("SHAPE CONTROLS: $shapes");

    for (var shape in shapes) {
      if (shape.control.type == "line") {
        drawLine(canvas, shape);
      } else if (shape.control.type == "circle") {
        drawCircle(canvas, shape);
      } else if (shape.control.type == "arc") {
        drawArc(canvas, shape);
      } else if (shape.control.type == "color") {
        drawColor(canvas, shape);
      } else if (shape.control.type == "oval") {
        drawOval(canvas, shape);
      } else if (shape.control.type == "paint") {
        drawPaint(canvas, shape);
      } else if (shape.control.type == "points") {
        drawPoints(canvas, shape);
      } else if (shape.control.type == "rect") {
        drawRect(canvas, shape);
      } else if (shape.control.type == "path") {
        drawPath(canvas, shape);
      }
    }
  }

  @override
  bool shouldRepaint(FletCustomPainter oldDelegate) {
    return true;
  }

  void drawLine(Canvas canvas, CustomPaintDrawShapeViewModel shape) {
    var p1 = parseOffset(shape.control, "p1")!;
    var p2 = parseOffset(shape.control, "p2")!;
    Paint paint = parsePaint(theme, shape.control, "paint");
    canvas.drawLine(Offset(p1.x, p1.y), Offset(p2.x, p2.y), paint);
  }

  void drawCircle(Canvas canvas, CustomPaintDrawShapeViewModel shape) {
    var center = parseOffset(shape.control, "center")!;
    var radius = shape.control.attrDouble("radius", 0)!;
    Paint paint = parsePaint(theme, shape.control, "paint");
    canvas.drawCircle(Offset(center.x, center.y), radius, paint);
  }

  void drawArc(Canvas canvas, CustomPaintDrawShapeViewModel shape) {
    var start = parseOffset(shape.control, "offset")!;
    var width = shape.control.attrDouble("width", 0)!;
    var height = shape.control.attrDouble("height", 0)!;
    var startAngle = shape.control.attrDouble("startAngle", 0)!;
    var sweepAngle = shape.control.attrDouble("sweepAngle", 0)!;
    var useCenter = shape.control.attrBool("useCenter", false)!;
    Paint paint = parsePaint(theme, shape.control, "paint");
    canvas.drawArc(Rect.fromLTWH(start.x, start.y, width, height), startAngle,
        sweepAngle, useCenter, paint);
  }

  void drawPaint(Canvas canvas, CustomPaintDrawShapeViewModel shape) {
    Paint paint = parsePaint(theme, shape.control, "paint");
    canvas.drawPaint(paint);
  }

  void drawColor(Canvas canvas, CustomPaintDrawShapeViewModel shape) {
    var color =
        HexColor.fromString(theme, shape.control.attrString("color", "")!) ??
            Colors.black;
    var blendMode = BlendMode.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            shape.control.attrString("blendMode", "")!.toLowerCase(),
        orElse: () => BlendMode.srcOver);
    canvas.drawColor(color, blendMode);
  }

  void drawOval(Canvas canvas, CustomPaintDrawShapeViewModel shape) {
    var start = parseOffset(shape.control, "offset")!;
    var width = shape.control.attrDouble("width", 0)!;
    var height = shape.control.attrDouble("height", 0)!;
    Paint paint = parsePaint(theme, shape.control, "paint");
    canvas.drawOval(Rect.fromLTWH(start.x, start.y, width, height), paint);
  }

  void drawPoints(Canvas canvas, CustomPaintDrawShapeViewModel shape) {
    var points = parseOffsetList(shape.control, "points")!;
    var pointMode = ui.PointMode.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            shape.control.attrString("pointMode", "")!.toLowerCase(),
        orElse: () => ui.PointMode.points);
    Paint paint = parsePaint(theme, shape.control, "paint");
    canvas.drawPoints(pointMode, points, paint);
  }

  void drawRect(Canvas canvas, CustomPaintDrawShapeViewModel shape) {
    var start = parseOffset(shape.control, "offset")!;
    var width = shape.control.attrDouble("width", 0)!;
    var height = shape.control.attrDouble("height", 0)!;
    var borderRadius = parseBorderRadius(shape.control, "borderRadius");
    Paint paint = parsePaint(theme, shape.control, "paint");
    canvas.drawRRect(
        RRect.fromRectAndCorners(Rect.fromLTWH(start.x, start.y, width, height),
            topLeft: borderRadius?.topLeft ?? Radius.zero,
            topRight: borderRadius?.topRight ?? Radius.zero,
            bottomLeft: borderRadius?.bottomLeft ?? Radius.zero,
            bottomRight: borderRadius?.bottomRight ?? Radius.zero),
        paint);
  }

  void drawPath(Canvas canvas, CustomPaintDrawShapeViewModel shape) {
    var path = buildPath(shape.shapes);
    Paint paint = parsePaint(theme, shape.control, "paint");
    canvas.drawPath(path, paint);
  }

  ui.Path buildPath(List<CustomPaintDrawShapeViewModel> shapes) {
    var path = ui.Path();
    for (var shape in shapes) {
      if (shape.control.type == "moveto") {
        path.moveTo(
            shape.control.attrDouble("x")!, shape.control.attrDouble("y")!);
      } else if (shape.control.type == "lineto") {
        path.lineTo(
            shape.control.attrDouble("x")!, shape.control.attrDouble("y")!);
      } else if (shape.control.type == "conicto") {
        path.conicTo(
            shape.control.attrDouble("x1")!,
            shape.control.attrDouble("y1")!,
            shape.control.attrDouble("x2")!,
            shape.control.attrDouble("y2")!,
            shape.control.attrDouble("w")!);
      } else if (shape.control.type == "cubicto") {
        path.cubicTo(
            shape.control.attrDouble("x1")!,
            shape.control.attrDouble("y1")!,
            shape.control.attrDouble("x2")!,
            shape.control.attrDouble("y2")!,
            shape.control.attrDouble("x3")!,
            shape.control.attrDouble("y3")!);
      } else if (shape.control.type == "bezierto") {
        path.quadraticBezierTo(
            shape.control.attrDouble("x1")!,
            shape.control.attrDouble("y1")!,
            shape.control.attrDouble("x2")!,
            shape.control.attrDouble("y2")!);
      } else if (shape.control.type == "close") {
        path.close();
      }
    }
    return path;
  }
}
