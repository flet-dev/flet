import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flet/src/extensions/control.dart';
import 'package:flet/src/utils/alignment.dart';
import 'package:flet/src/utils/borders.dart';
import 'package:flet/src/utils/colors.dart';
import 'package:flet/src/utils/drawing.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../models/control.dart';
import '../utils/dash_path.dart';
import '../utils/hashing.dart';
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
  Size _lastSize = Size.zero;
  ui.Image? _capturedImage;
  double _dpr = 1.0;
  bool _initialized = false;

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (!_initialized) {
      _dpr = MediaQuery.devicePixelRatioOf(context);
      _initialized = true;
    }
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<void> _awaitImageLoads(List<Control> shapes) async {
    final pending = <Future>[];

    for (final shape in shapes) {
      if (shape.type == "Image") {
        if (shape.get("_loading") != null) {
          pending.add(shape.get("_loading").future);
        } else if (shape.get("_image") == null ||
            shape.get("_hash") != getImageHash(shape)) {
          final future = loadCanvasImage(shape);
          pending.add(future);
        }
      }
    }

    if (pending.isNotEmpty) {
      await Future.wait(pending);
    }
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Canvas.$name($args)");
    switch (name) {
      case "capture":
        final shapes = widget.control.children("shapes");
        if (_lastSize.isEmpty || shapes.isEmpty) {
          return;
        }

        // Wait for all images to load
        await _awaitImageLoads(shapes);

        if (!mounted) return;

        final recorder = ui.PictureRecorder();
        final canvas = Canvas(recorder);

        final painter = FletCustomPainter(
            context: context,
            theme: Theme.of(context),
            shapes: shapes,
            capturedImage: _capturedImage,
            onPaintCallback: (_) {},
            dpr: _dpr);

        painter.paint(canvas, _lastSize);

        final picture = recorder.endRecording();
        _capturedImage = await picture.toImage(
          (_lastSize.width * _dpr).toInt(),
          (_lastSize.height * _dpr).toInt(),
        );
        return;

      case "get_capture":
        if (_capturedImage == null) return null;
        final byteData =
            await _capturedImage!.toByteData(format: ui.ImageByteFormat.png);
        return byteData!.buffer.asUint8List();

      case "clear_capture":
        _capturedImage?.dispose();
        _capturedImage = null;
        setState(() {});
        return;

      default:
        throw Exception("Unknown Canvas method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Canvas build: ${widget.control.id}");

    var resizeInterval = widget.control.getInt("resize_interval", 10)!;

    var paint = CustomPaint(
      painter: FletCustomPainter(
        context: context,
        theme: Theme.of(context),
        shapes: widget.control.children("shapes"),
        capturedImage: _capturedImage,
        dpr: 1,
        onPaintCallback: (size) {
          var now = DateTime.now().millisecondsSinceEpoch;
          if ((now - _lastResize > resizeInterval && _lastSize != size) ||
              _lastSize.isEmpty) {
            _lastSize = size;
            _lastResize = now;
            widget.control
                .triggerEvent("resize", {"w": size.width, "h": size.height});
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
  final ui.Image? capturedImage;
  final double dpr;

  const FletCustomPainter({
    required this.context,
    required this.theme,
    required this.shapes,
    required this.onPaintCallback,
    required this.dpr,
    this.capturedImage,
  });

  @override
  void paint(Canvas canvas, Size size) {
    onPaintCallback(size);

    debugPrint("paint.size: $size");
    //debugPrint("paint.shapes: $shapes");

    canvas.save();
    canvas.scale(dpr);
    canvas.clipRect(Rect.fromLTWH(0, 0, size.width, size.height));

    if (capturedImage != null) {
      final src = Rect.fromLTWH(0, 0, capturedImage!.width.toDouble(),
          capturedImage!.height.toDouble());
      final dst = Rect.fromLTWH(0, 0, size.width, size.height);
      canvas.drawImageRect(capturedImage!, src, dst, Paint());
    }

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
      } else if (shape.type == "Image") {
        drawImage(canvas, shape);
      }
    }

    canvas.restore();
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
    var color = shape.getColor("color", context) ?? Colors.black;
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
    var borderRadius = shape.getBorderRadius("border_radius");
    Paint paint = shape.getPaint("paint", theme, Paint())!;
    canvas.drawRRect(
        RRect.fromRectAndCorners(
            Rect.fromLTWH(
                shape.getDouble("x")!, shape.getDouble("y")!, width, height),
            topLeft: borderRadius?.topLeft ?? Radius.zero,
            topRight: borderRadius?.topRight ?? Radius.zero,
            bottomLeft: borderRadius?.bottomLeft ?? Radius.zero,
            bottomRight: borderRadius?.bottomRight ?? Radius.zero),
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
        textAlign:
            parseTextAlign(shape.getString("text_align"), TextAlign.start)!,
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
    var color = shape.getColor("color", context) ?? Colors.black;
    var elevation = shape.getDouble("elevation", 0)!;
    var transparentOccluder = shape.getBool("transparent_occluder", false)!;
    canvas.drawShadow(path, color, elevation, transparentOccluder);
  }

  void drawImage(Canvas canvas, Control shape) {
    final paint = shape.getPaint("paint", theme, Paint())!;
    final x = shape.getDouble("x")!;
    final y = shape.getDouble("y")!;
    final width = shape.getDouble("width");
    final height = shape.getDouble("height");

    // Check if image is already loaded and stored
    if (shape.get("_image") != null &&
        shape.get("_hash") == getImageHash(shape)) {
      final img = shape.get("_image")!;
      final srcRect =
          Rect.fromLTWH(0, 0, img.width.toDouble(), img.height.toDouble());
      final dstRect = width != null && height != null
          ? Rect.fromLTWH(x, y, width, height)
          : Offset(x, y) & Size(img.width.toDouble(), img.height.toDouble());
      debugPrint("canvas.drawImageRect($srcRect, $dstRect)");
      canvas.drawImageRect(img, srcRect, dstRect, paint);
    } else {
      loadCanvasImage(shape);
    }
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

Future<void> loadCanvasImage(Control shape) async {
  debugPrint("loadCanvasImage(${shape.id})");
  if (shape.get("_loading") != null) return;
  final completer = Completer();
  shape.properties["_loading"] = completer;

  final src = shape.getString("src");
  final srcBytes = shape.get("src_bytes") as Uint8List?;

  try {
    Uint8List bytes;

    if (srcBytes != null) {
      bytes = srcBytes;
    } else if (src != null) {
      var assetSrc = shape.backend.getAssetSource(src);
      if (assetSrc.isFile) {
        final file = File(assetSrc.path);
        bytes = await file.readAsBytes();
      } else {
        final resp = await http.get(Uri.parse(assetSrc.path));
        if (resp.statusCode != 200) {
          throw Exception("HTTP ${resp.statusCode}");
        }
        bytes = resp.bodyBytes;
      }
    } else if (src != null) {
      bytes = base64Decode(src);
    } else {
      throw Exception("Missing image source: 'src' or 'src_bytes'");
    }

    final codec = await ui.instantiateImageCodec(bytes);
    final frame = await codec.getNextFrame();
    shape.properties["_image"] = frame.image;
    shape.updateProperties({"_hash": getImageHash(shape)},
        python: false, notify: true);
    completer.complete();
  } catch (e) {
    shape.properties["_image_error"] = e;
    completer.completeError(e);
  } finally {
    shape.properties.remove("_loading");
  }
}

int getImageHash(Control shape) {
  final src = shape.getString("src");
  final srcBytes = shape.get("src_bytes") as Uint8List?;
  return src != null
      ? src.hashCode
      : srcBytes != null
          ? fnv1aHash(srcBytes)
          : 0;
}
