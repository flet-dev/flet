import 'dart:ui' as ui;

import 'package:flet/src/extensions/control.dart';
import 'package:flet/src/utils/alignment.dart';
import 'package:flet/src/utils/borders.dart';
import 'package:flet/src/utils/colors.dart';
import 'package:flet/src/utils/drawing.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/dash_path.dart';
import '../utils/images.dart';
import '../utils/text.dart';
import '../utils/transforms.dart';
import 'base_controls.dart';

typedef CanvasControlOnPaintCallback = void Function(Size size);

class CanvasControl extends StatefulWidget {
  final Control control;

  CanvasControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<CanvasControl> createState() => _CanvasControlState();
}

class _CanvasControlState extends State<CanvasControl> {
  int _lastResize = DateTime.now().millisecondsSinceEpoch;
  Size? _lastSize;

  @override
  Widget build(BuildContext context) {
    debugPrint("Canvas build: ${widget.control.id}");

    var onResize = widget.control.getBool("on_resize", false)!;
    var resizeInterval = widget.control.getInt("resize_interval", 10)!;

    var paint = CustomPaint(
      painter: FletCustomPainter(
        context: context,
        theme: Theme.of(context),
        shapes: widget.control.children("shapes"),
        onPaintCallback: (size) {
          if (onResize) {
            var now = DateTime.now().millisecondsSinceEpoch;
            if ((now - _lastResize > resizeInterval && _lastSize != size) ||
                _lastSize == null) {
              _lastResize = now;
              _lastSize = size;
              widget.control
                  .triggerEvent("resize", {"w": size.width, "h": size.height});
            }
          }
        },
      ),
      child: widget.control.buildWidget("content"),
    );

    return ConstrainedControl(control: widget.control, child: paint);
  }
}

class FletCustomPainter extends CustomPainter {
  final BuildContext context;
  final ThemeData theme;
  final List<Control> shapes;
  final CanvasControlOnPaintCallback onPaintCallback;

  const FletCustomPainter(
      {required this.context,
      required this.theme,
      required this.shapes,
      required this.onPaintCallback});

  @override
  void paint(Canvas canvas, Size size) {
    onPaintCallback(size);

    //debugPrint("SHAPE CONTROLS: $shapes");

    for (var shape in shapes) {
      shape.notifyParent = true;
      if (shape.type == "Line") {
        drawLine(canvas, shape);
      } else if (shape.type == "Circle") {
        drawCircle(canvas, shape);
      } else if (shape.type == "Arc") {
        drawArc(canvas, shape);
      } else if (shape.type == "Color") {
        drawColor(canvas, shape);
      } else if (shape.type == "Oval") {
        drawOval(canvas, shape);
      } else if (shape.type == "Fill") {
        drawFill(canvas, shape);
      } else if (shape.type == "Points") {
        drawPoints(canvas, shape);
      } else if (shape.type == "Rect") {
        drawRect(canvas, shape);
      } else if (shape.type == "Path") {
        drawPath(canvas, shape);
      } else if (shape.type == "Shadow") {
        drawShadow(canvas, shape);
      } else if (shape.type == "Text") {
        drawText(context, canvas, shape);
      }
    }
  }

  @override
  bool shouldRepaint(FletCustomPainter oldPainter) {
    return true;
  }

  void drawLine(Canvas canvas, Control shape) {
    Paint paint = shape.getPaint("paint", theme, Paint())!;
    var dashPattern = shape.getPaintStrokeDashPattern("paint");
    paint.style = ui.PaintingStyle.stroke;
    var path = ui.Path();
    path.moveTo(shape.getDouble("x1")!, shape.getDouble("y1")!);
    path.lineTo(shape.getDouble("x2")!, shape.getDouble("y2")!);

    if (dashPattern != null) {
      path = dashPath(path, dashArray: CircularIntervalList(dashPattern));
    }
    canvas.drawPath(path, paint);
  }

  void drawCircle(Canvas canvas, Control shape) {
    var radius = shape.getDouble("radius", 0)!;
    Paint paint = shape.getPaint("paint", theme, Paint())!;
    canvas.drawCircle(
        Offset(shape.getDouble("x")!, shape.getDouble("y")!), radius, paint);
  }

  void drawOval(Canvas canvas, Control shape) {
    var width = shape.getDouble("width", 0)!;
    var height = shape.getDouble("height", 0)!;
    Paint paint = shape.getPaint("paint", theme, Paint())!;
    canvas.drawOval(
        Rect.fromLTWH(
            shape.getDouble("x")!, shape.getDouble("y")!, width, height),
        paint);
  }

  void drawArc(Canvas canvas, Control shape) {
    var width = shape.getDouble("width", 0)!;
    var height = shape.getDouble("height", 0)!;
    var startAngle = shape.getDouble("start_angle", 0)!;
    var sweepAngle = shape.getDouble("sweep_angle", 0)!;
    var useCenter = shape.getBool("use_center", false)!;
    Paint paint = shape.getPaint("paint", theme, Paint())!;
    canvas.drawArc(
        Rect.fromLTWH(
            shape.getDouble("x")!, shape.getDouble("y")!, width, height),
        startAngle,
        sweepAngle,
        useCenter,
        paint);
  }

  void drawFill(Canvas canvas, Control shape) {
    Paint paint = shape.getPaint("paint", theme, Paint())!;
    canvas.drawPaint(paint);
  }

  void drawColor(Canvas canvas, Control shape) {
    var color = shape.getColor("color", context, Colors.black)!;
    var blendMode =
        parseBlendMode(shape.getString("blend_mode"), BlendMode.srcOver)!;
    canvas.drawColor(color, blendMode);
  }

  void drawPoints(Canvas canvas, Control shape) {
    var points = parseOffsetList(shape.get("points"))!;
    var pointMode = ui.PointMode.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            shape.getString("point_mode", "")!.toLowerCase(),
        orElse: () => ui.PointMode.points);
    Paint paint = shape.getPaint("paint", theme, Paint())!;
    canvas.drawPoints(pointMode, points, paint);
  }

  void drawRect(Canvas canvas, Control shape) {
    var width = shape.getDouble("width", 0)!;
    var height = shape.getDouble("height", 0)!;
    var borderRadius =
        shape.getBorderRadius("border_radius", BorderRadius.zero)!;
    Paint paint = shape.getPaint("paint", theme, Paint())!;
    canvas.drawRRect(
        RRect.fromRectAndCorners(
            Rect.fromLTWH(
                shape.getDouble("x")!, shape.getDouble("y")!, width, height),
            topLeft: borderRadius.topLeft,
            topRight: borderRadius.topRight,
            bottomLeft: borderRadius.bottomLeft,
            bottomRight: borderRadius.bottomRight),
        paint);
  }

  void drawText(BuildContext context, Canvas canvas, Control shape) {
    var offset = Offset(shape.getDouble("x")!, shape.getDouble("y")!);
    var alignment = shape.getAlignment("alignment", Alignment.topLeft)!;
    var style =
        shape.getTextStyle("style", theme, theme.textTheme.bodyMedium!)!;
    if (style.color == null) {
      style = style.copyWith(color: theme.textTheme.bodyMedium!.color);
    }
    TextSpan span = TextSpan(
        text: shape.getString("text", "")!,
        style: style,
        children: parseTextSpans(shape.children("spans"), theme));

    var maxLines = shape.getInt("max_lines");
    var maxWidth = shape.getDouble("max_width");
    var ellipsis = shape.getString("ellipsis");

    // paint
    TextPainter textPainter = TextPainter(
        text: span,
        textAlign: shape.getTextAlign("text_align", TextAlign.start)!,
        maxLines: maxLines,
        ellipsis: ellipsis,
        textDirection: Directionality.of(context));
    textPainter.layout(maxWidth: maxWidth ?? double.infinity);

    var angle = shape.getDouble("rotate", 0)!;

    final delta = Offset(
        offset.dx - textPainter.size.width / 2 * (alignment.x + 1.0),
        offset.dy - textPainter.size.height / 2 * (alignment.y + 1.0));

    // rotate the text around offset point
    canvas.save();
    canvas.translate(offset.dx, offset.dy);
    canvas.rotate(angle);
    canvas.translate(-offset.dx, -offset.dy);
    textPainter.paint(canvas, delta);
    canvas.restore();
  }

  void drawPath(Canvas canvas, Control shape) {
    var path = buildPath(shape.get("elements", [])!);
    Paint paint = shape.getPaint("paint", theme, Paint())!;
    var dashPattern = shape.getPaintStrokeDashPattern("paint");
    if (dashPattern != null) {
      path = dashPath(path, dashArray: CircularIntervalList(dashPattern));
    }
    canvas.drawPath(path, paint);
  }

  void drawShadow(Canvas canvas, Control shape) {
    var path = buildPath(shape.get("path", [])!);
    var color = shape.getColor("color", context, Colors.black)!;
    var elevation = shape.getDouble("elevation", 0)!;
    var transparentOccluder = shape.getBool("transparent_occluder", false)!;
    canvas.drawShadow(path, color, elevation, transparentOccluder);
  }

  ui.Path buildPath(dynamic j) {
    var path = ui.Path();
    if (j == null) {
      return path;
    }
    for (var elem in (j as List)) {
      var type = elem["_type"];
      if (type == "moveto") {
        path.moveTo(parseDouble(elem["x"], 0)!, parseDouble(elem["y"], 0)!);
      } else if (type == "lineto") {
        path.lineTo(parseDouble(elem["x"], 0)!, parseDouble(elem["y"], 0)!);
      } else if (type == "arc") {
        path.addArc(
            Rect.fromLTWH(
                parseDouble(elem["x"], 0)!,
                parseDouble(elem["y"], 0)!,
                parseDouble(elem["width"], 0)!,
                parseDouble(elem["height"], 0)!),
            parseDouble(elem["start_angle"], 0)!,
            parseDouble(elem["sweep_angle"], 0)!);
      } else if (type == "arcto") {
        path.arcToPoint(
            Offset(parseDouble(elem["x"], 0)!, parseDouble(elem["y"], 0)!),
            radius: Radius.circular(parseDouble(elem["radius"], 0)!),
            rotation: parseDouble(elem["rotation"], 0)!,
            largeArc: parseBool(elem["large_arc"], false)!,
            clockwise: parseBool(elem["clockwise"], true)!);
      } else if (type == "oval") {
        path.addOval(Rect.fromLTWH(
            parseDouble(elem["x"], 0)!,
            parseDouble(elem["y"], 0)!,
            parseDouble(elem["width"], 0)!,
            parseDouble(elem["height"], 0)!));
      } else if (type == "rect") {
        var borderRadius = parseBorderRadius(elem["border_radius"]);
        path.addRRect(RRect.fromRectAndCorners(
            Rect.fromLTWH(
                parseDouble(elem["x"], 0)!,
                parseDouble(elem["y"], 0)!,
                parseDouble(elem["width"], 0)!,
                parseDouble(elem["height"], 0)!),
            topLeft: borderRadius?.topLeft ?? Radius.zero,
            topRight: borderRadius?.topRight ?? Radius.zero,
            bottomLeft: borderRadius?.bottomLeft ?? Radius.zero,
            bottomRight: borderRadius?.bottomRight ?? Radius.zero));
      } else if (type == "conicto") {
        path.conicTo(
            parseDouble(elem["cp1x"], 0)!,
            parseDouble(elem["cp1y"], 0)!,
            parseDouble(elem["x"], 0)!,
            parseDouble(elem["y"], 0)!,
            parseDouble(elem["w"], 0)!);
      } else if (type == "cubicto") {
        path.cubicTo(
            parseDouble(elem["cp1x"], 0)!,
            parseDouble(elem["cp1y"], 0)!,
            parseDouble(elem["cp2x"], 0)!,
            parseDouble(elem["cp2y"], 0)!,
            parseDouble(elem["x"], 0)!,
            parseDouble(elem["y"], 0)!);
      } else if (type == "subpath") {
        path.addPath(buildPath(elem["elements"]),
            Offset(parseDouble(elem["x"], 0)!, parseDouble(elem["y"], 0)!));
      } else if (type == "close") {
        path.close();
      }
    }
    return path;
  }
}
