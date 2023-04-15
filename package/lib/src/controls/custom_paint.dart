import 'dart:convert';

import 'package:flet/src/utils/transforms.dart';
import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
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

    var contentCtrls = widget.children.where((c) => c.isVisible);

    var onResize = widget.control.attrBool("onResize", false)!;
    var resizeInterval = widget.control.attrInt("resizeInterval", 10)!;

    var paint = CustomPaint(
      painter: FletCustomPainter(
        controls: contentCtrls,
        onPaintCallback: (size) {
          if (onResize) {
            var now = DateTime.now().millisecondsSinceEpoch;
            if ((now - _lastResize > resizeInterval && _lastSize != size) ||
                _lastSize == null) {
              _lastResize = now;
              _lastSize = size;
              FletAppServices.of(context).server.sendPageEvent(
                  eventTarget: widget.control.id,
                  eventName: "resize",
                  eventData: json.encode({"w": size.width, "h": size.height}));
            }
          }
        },
      ),
    );

    return constrainedControl(context, paint, widget.parent, widget.control);
  }
}

class FletCustomPainter extends CustomPainter {
  final Iterable<Control> controls;
  final CustomPaintControlOnPaintCallback onPaintCallback;

  const FletCustomPainter(
      {required this.controls, required this.onPaintCallback});

  @override
  void paint(Canvas canvas, Size size) {
    onPaintCallback(size);

    debugPrint("SHAPE CONTROLS: $controls");

    for (var c in controls) {
      if (c.type == "line") {
        drawLine(canvas, c);
      } else if (c.type == "circle") {
        drawCircle(canvas, c);
      }
    }

    // // 1
    // Offset startPoint = Offset(0, 0);
    // // 2
    // Offset endPoint = Offset(size.width, size.height);
    // // 3
    // Paint paint = Paint();
    // // 4
    // canvas.drawLine(startPoint, endPoint, paint);
  }

  @override
  bool shouldRepaint(FletCustomPainter oldDelegate) {
    return true;
  }

  void drawLine(Canvas canvas, Control c) {
    var p1 = parseOffset(c, "p1")!;
    var p2 = parseOffset(c, "p2")!;
    Paint paint = Paint();
    canvas.drawLine(Offset(p1.x, p1.y), Offset(p2.x, p2.y), paint);
  }

  void drawCircle(Canvas canvas, Control c) {
    var center = parseOffset(c, "center")!;
    var radius = c.attrDouble("radius", 0)!;
    Paint paint = Paint();
    canvas.drawCircle(Offset(center.x, center.y), radius, paint);
  }
}
