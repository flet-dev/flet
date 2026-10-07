// The components of HSV Color Picker
//
// Try to create a Color Picker with other layout on your own :)

import 'dart:math';
import 'package:flutter/gestures.dart';
import 'package:material_ui/material_ui.dart';
import 'package:flutter/services.dart';
import 'utils.dart';

/// Palette types for color picker area widget.
enum PaletteType {
  hsv,
  hsvWithHue,
  hsvWithValue,
  hsvWithSaturation,
  hsl,
  hslWithHue,
  hslWithLightness,
  hslWithSaturation,
  rgbWithBlue,
  rgbWithGreen,
  rgbWithRed,
  hueWheel,
}

/// Track types for slider picker.
enum TrackType {
  hue,
  saturation,
  saturationForHSL,
  value,
  lightness,
  red,
  green,
  blue,
  alpha,
}

/// Color information label type.
enum ColorLabelType { hex, rgb, hsv, hsl }

/// Types for slider picker widget.
enum ColorModel { rgb, hsv, hsl }
// enum ColorSpace { rgb, hsv, hsl, hsp, okhsv, okhsl, xyz, yuv, lab, lch, cmyk }

/// Painter for SV mixture.
class HSVWithHueColorPainter extends CustomPainter {
  const HSVWithHueColorPainter(this.hsvColor, {this.pointerColor});

  final HSVColor hsvColor;
  final Color? pointerColor;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    const Gradient gradientV = LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [Colors.white, Colors.black],
    );
    final Gradient gradientH = LinearGradient(
      colors: [
        Colors.white,
        HSVColor.fromAHSV(1.0, hsvColor.hue, 1.0, 1.0).toColor(),
      ],
    );
    canvas.drawRect(rect, Paint()..shader = gradientV.createShader(rect));
    canvas.drawRect(
      rect,
      Paint()
        ..blendMode = BlendMode.multiply
        ..shader = gradientH.createShader(rect),
    );

    canvas.drawCircle(
      Offset(size.width * hsvColor.saturation, size.height * (1 - hsvColor.value)),
      size.height * 0.04,
      Paint()
        ..color = pointerColor ?? (useWhiteForeground(hsvColor.toColor()) ? Colors.white : Colors.black)
        ..strokeWidth = 1.5
        ..blendMode = BlendMode.luminosity
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for HV mixture.
class HSVWithSaturationColorPainter extends CustomPainter {
  const HSVWithSaturationColorPainter(this.hsvColor, {this.pointerColor});

  final HSVColor hsvColor;
  final Color? pointerColor;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    const Gradient gradientV = LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [Colors.transparent, Colors.black],
    );
    final List<Color> colors = [
      HSVColor.fromAHSV(1.0, 0.0, hsvColor.saturation, 1.0).toColor(),
      HSVColor.fromAHSV(1.0, 60.0, hsvColor.saturation, 1.0).toColor(),
      HSVColor.fromAHSV(1.0, 120.0, hsvColor.saturation, 1.0).toColor(),
      HSVColor.fromAHSV(1.0, 180.0, hsvColor.saturation, 1.0).toColor(),
      HSVColor.fromAHSV(1.0, 240.0, hsvColor.saturation, 1.0).toColor(),
      HSVColor.fromAHSV(1.0, 300.0, hsvColor.saturation, 1.0).toColor(),
      HSVColor.fromAHSV(1.0, 360.0, hsvColor.saturation, 1.0).toColor(),
    ];
    final Gradient gradientH = LinearGradient(colors: colors);
    canvas.drawRect(rect, Paint()..shader = gradientH.createShader(rect));
    canvas.drawRect(rect, Paint()..shader = gradientV.createShader(rect));

    canvas.drawCircle(
      Offset(
        size.width * hsvColor.hue / 360,
        size.height * (1 - hsvColor.value),
      ),
      size.height * 0.04,
      Paint()
        ..color = pointerColor ?? (useWhiteForeground(hsvColor.toColor()) ? Colors.white : Colors.black)
        ..strokeWidth = 1.5
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for HS mixture.
class HSVWithValueColorPainter extends CustomPainter {
  const HSVWithValueColorPainter(this.hsvColor, {this.pointerColor});

  final HSVColor hsvColor;
  final Color? pointerColor;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    const Gradient gradientV = LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [Colors.transparent, Colors.white],
    );
    final List<Color> colors = [
      const HSVColor.fromAHSV(1.0, 0.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 60.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 120.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 180.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 240.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 300.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 360.0, 1.0, 1.0).toColor(),
    ];
    final Gradient gradientH = LinearGradient(colors: colors);
    canvas.drawRect(rect, Paint()..shader = gradientH.createShader(rect));
    canvas.drawRect(rect, Paint()..shader = gradientV.createShader(rect));
    canvas.drawRect(
      rect,
      Paint()..color = Colors.black.withOpacity(1 - hsvColor.value),
    );

    canvas.drawCircle(
      Offset(
        size.width * hsvColor.hue / 360,
        size.height * (1 - hsvColor.saturation),
      ),
      size.height * 0.04,
      Paint()
        ..color = pointerColor ?? (useWhiteForeground(hsvColor.toColor()) ? Colors.white : Colors.black)
        ..strokeWidth = 1.5
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for SL mixture.
class HSLWithHueColorPainter extends CustomPainter {
  const HSLWithHueColorPainter(this.hslColor, {this.pointerColor});

  final HSLColor hslColor;
  final Color? pointerColor;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    final Gradient gradientH = LinearGradient(
      colors: [
        const Color(0xff808080),
        HSLColor.fromAHSL(1.0, hslColor.hue, 1.0, 0.5).toColor(),
      ],
    );
    const Gradient gradientV = LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      stops: [0.0, 0.5, 0.5, 1],
      colors: [
        Colors.white,
        Color(0x00ffffff),
        Colors.transparent,
        Colors.black,
      ],
    );
    canvas.drawRect(rect, Paint()..shader = gradientH.createShader(rect));
    canvas.drawRect(rect, Paint()..shader = gradientV.createShader(rect));

    canvas.drawCircle(
      Offset(size.width * hslColor.saturation, size.height * (1 - hslColor.lightness)),
      size.height * 0.04,
      Paint()
        ..color = pointerColor ?? (useWhiteForeground(hslColor.toColor()) ? Colors.white : Colors.black)
        ..strokeWidth = 1.5
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for HL mixture.
class HSLWithSaturationColorPainter extends CustomPainter {
  const HSLWithSaturationColorPainter(this.hslColor, {this.pointerColor});

  final HSLColor hslColor;
  final Color? pointerColor;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    final List<Color> colors = [
      HSLColor.fromAHSL(1.0, 0.0, hslColor.saturation, 0.5).toColor(),
      HSLColor.fromAHSL(1.0, 60.0, hslColor.saturation, 0.5).toColor(),
      HSLColor.fromAHSL(1.0, 120.0, hslColor.saturation, 0.5).toColor(),
      HSLColor.fromAHSL(1.0, 180.0, hslColor.saturation, 0.5).toColor(),
      HSLColor.fromAHSL(1.0, 240.0, hslColor.saturation, 0.5).toColor(),
      HSLColor.fromAHSL(1.0, 300.0, hslColor.saturation, 0.5).toColor(),
      HSLColor.fromAHSL(1.0, 360.0, hslColor.saturation, 0.5).toColor(),
    ];
    final Gradient gradientH = LinearGradient(colors: colors);
    const Gradient gradientV = LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      stops: [0.0, 0.5, 0.5, 1],
      colors: [
        Colors.white,
        Color(0x00ffffff),
        Colors.transparent,
        Colors.black,
      ],
    );
    canvas.drawRect(rect, Paint()..shader = gradientH.createShader(rect));
    canvas.drawRect(rect, Paint()..shader = gradientV.createShader(rect));

    canvas.drawCircle(
      Offset(size.width * hslColor.hue / 360, size.height * (1 - hslColor.lightness)),
      size.height * 0.04,
      Paint()
        ..color = pointerColor ?? (useWhiteForeground(hslColor.toColor()) ? Colors.white : Colors.black)
        ..strokeWidth = 1.5
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for HS mixture.
class HSLWithLightnessColorPainter extends CustomPainter {
  const HSLWithLightnessColorPainter(this.hslColor, {this.pointerColor});

  final HSLColor hslColor;
  final Color? pointerColor;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    final List<Color> colors = [
      const HSLColor.fromAHSL(1.0, 0.0, 1.0, 0.5).toColor(),
      const HSLColor.fromAHSL(1.0, 60.0, 1.0, 0.5).toColor(),
      const HSLColor.fromAHSL(1.0, 120.0, 1.0, 0.5).toColor(),
      const HSLColor.fromAHSL(1.0, 180.0, 1.0, 0.5).toColor(),
      const HSLColor.fromAHSL(1.0, 240.0, 1.0, 0.5).toColor(),
      const HSLColor.fromAHSL(1.0, 300.0, 1.0, 0.5).toColor(),
      const HSLColor.fromAHSL(1.0, 360.0, 1.0, 0.5).toColor(),
    ];
    final Gradient gradientH = LinearGradient(colors: colors);
    const Gradient gradientV = LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [
        Colors.transparent,
        Color(0xFF808080),
      ],
    );
    canvas.drawRect(rect, Paint()..shader = gradientH.createShader(rect));
    canvas.drawRect(rect, Paint()..shader = gradientV.createShader(rect));
    canvas.drawRect(
      rect,
      Paint()..color = Colors.black.withOpacity((1 - hslColor.lightness * 2).clamp(0, 1)),
    );
    canvas.drawRect(
      rect,
      Paint()..color = Colors.white.withOpacity(((hslColor.lightness - 0.5) * 2).clamp(0, 1)),
    );

    canvas.drawCircle(
      Offset(size.width * hslColor.hue / 360, size.height * (1 - hslColor.saturation)),
      size.height * 0.04,
      Paint()
        ..color = pointerColor ?? (useWhiteForeground(hslColor.toColor()) ? Colors.white : Colors.black)
        ..strokeWidth = 1.5
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for GB mixture.
class RGBWithRedColorPainter extends CustomPainter {
  const RGBWithRedColorPainter(this.color, {this.pointerColor});

  final Color color;
  final Color? pointerColor;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    final Gradient gradientH = LinearGradient(
      colors: [
        Color.fromRGBO(color.red, 255, 0, 1.0),
        Color.fromRGBO(color.red, 255, 255, 1.0),
      ],
    );
    final Gradient gradientV = LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [
        Color.fromRGBO(color.red, 255, 255, 1.0),
        Color.fromRGBO(color.red, 0, 255, 1.0),
      ],
    );
    canvas.drawRect(rect, Paint()..shader = gradientH.createShader(rect));
    canvas.drawRect(
      rect,
      Paint()
        ..shader = gradientV.createShader(rect)
        ..blendMode = BlendMode.multiply,
    );

    canvas.drawCircle(
      Offset(size.width * color.blue / 255, size.height * (1 - color.green / 255)),
      size.height * 0.04,
      Paint()
        ..color = pointerColor ?? (useWhiteForeground(color) ? Colors.white : Colors.black)
        ..strokeWidth = 1.5
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for RB mixture.
class RGBWithGreenColorPainter extends CustomPainter {
  const RGBWithGreenColorPainter(this.color, {this.pointerColor});

  final Color color;
  final Color? pointerColor;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    final Gradient gradientH = LinearGradient(
      colors: [
        Color.fromRGBO(255, color.green, 0, 1.0),
        Color.fromRGBO(255, color.green, 255, 1.0),
      ],
    );
    final Gradient gradientV = LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [
        Color.fromRGBO(255, color.green, 255, 1.0),
        Color.fromRGBO(0, color.green, 255, 1.0),
      ],
    );
    canvas.drawRect(rect, Paint()..shader = gradientH.createShader(rect));
    canvas.drawRect(
      rect,
      Paint()
        ..shader = gradientV.createShader(rect)
        ..blendMode = BlendMode.multiply,
    );

    canvas.drawCircle(
      Offset(size.width * color.blue / 255, size.height * (1 - color.red / 255)),
      size.height * 0.04,
      Paint()
        ..color = pointerColor ?? (useWhiteForeground(color) ? Colors.white : Colors.black)
        ..strokeWidth = 1.5
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for RG mixture.
class RGBWithBlueColorPainter extends CustomPainter {
  const RGBWithBlueColorPainter(this.color, {this.pointerColor});

  final Color color;
  final Color? pointerColor;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    final Gradient gradientH = LinearGradient(
      colors: [
        Color.fromRGBO(0, 255, color.blue, 1.0),
        Color.fromRGBO(255, 255, color.blue, 1.0),
      ],
    );
    final Gradient gradientV = LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [
        Color.fromRGBO(255, 255, color.blue, 1.0),
        Color.fromRGBO(255, 0, color.blue, 1.0),
      ],
    );
    canvas.drawRect(rect, Paint()..shader = gradientH.createShader(rect));
    canvas.drawRect(
      rect,
      Paint()
        ..shader = gradientV.createShader(rect)
        ..blendMode = BlendMode.multiply,
    );

    canvas.drawCircle(
      Offset(size.width * color.red / 255, size.height * (1 - color.green / 255)),
      size.height * 0.04,
      Paint()
        ..color = pointerColor ?? (useWhiteForeground(color) ? Colors.white : Colors.black)
        ..strokeWidth = 1.5
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for hue color wheel.
class HUEColorWheelPainter extends CustomPainter {
  const HUEColorWheelPainter(this.hsvColor, {this.pointerColor});

  final HSVColor hsvColor;
  final Color? pointerColor;

  @override
  void paint(Canvas canvas, Size size) {
    Rect rect = Offset.zero & size;
    Offset center = Offset(size.width / 2, size.height / 2);
    double radio = size.width <= size.height ? size.width / 2 : size.height / 2;

    final List<Color> colors = [
      const HSVColor.fromAHSV(1.0, 360.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 300.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 240.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 180.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 120.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 60.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 0.0, 1.0, 1.0).toColor(),
    ];
    final Gradient gradientS = SweepGradient(colors: colors);
    const Gradient gradientR = RadialGradient(
      colors: [
        Colors.white,
        Color(0x00FFFFFF),
      ],
    );
    canvas.drawCircle(center, radio, Paint()..shader = gradientS.createShader(rect));
    canvas.drawCircle(center, radio, Paint()..shader = gradientR.createShader(rect));
    canvas.drawCircle(center, radio, Paint()..color = Colors.black.withOpacity(1 - hsvColor.value));

    canvas.drawCircle(
      Offset(
        center.dx + hsvColor.saturation * radio * cos((hsvColor.hue * pi / 180)),
        center.dy - hsvColor.saturation * radio * sin((hsvColor.hue * pi / 180)),
      ),
      size.height * 0.04,
      Paint()
        ..color = pointerColor ?? (useWhiteForeground(hsvColor.toColor()) ? Colors.white : Colors.black)
        ..strokeWidth = 1.5
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for hue ring.
class HueRingPainter extends CustomPainter {
  const HueRingPainter(this.hsvColor, {this.displayThumbColor = true, this.strokeWidth = 5});

  final HSVColor hsvColor;
  final bool displayThumbColor;
  final double strokeWidth;

  @override
  void paint(Canvas canvas, Size size) {
    Rect rect = Offset.zero & size;
    Offset center = Offset(size.width / 2, size.height / 2);
    double radio = size.width <= size.height ? size.width / 2 : size.height / 2;

    final List<Color> colors = [
      const HSVColor.fromAHSV(1.0, 360.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 300.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 240.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 180.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 120.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 60.0, 1.0, 1.0).toColor(),
      const HSVColor.fromAHSV(1.0, 0.0, 1.0, 1.0).toColor(),
    ];
    canvas.drawCircle(
      center,
      radio,
      Paint()
        ..shader = SweepGradient(colors: colors).createShader(rect)
        ..style = PaintingStyle.stroke
        ..strokeWidth = strokeWidth,
    );

    final Offset offset = Offset(
      center.dx + radio * cos((hsvColor.hue * pi / 180)),
      center.dy - radio * sin((hsvColor.hue * pi / 180)),
    );
    canvas.drawShadow(Path()..addOval(Rect.fromCircle(center: offset, radius: 12)), Colors.black, 3.0, true);
    canvas.drawCircle(
      offset,
      size.height * 0.04,
      Paint()
        ..color = Colors.white
        ..style = PaintingStyle.fill,
    );
    if (displayThumbColor) {
      canvas.drawCircle(
        offset,
        size.height * 0.03,
        Paint()
          ..color = hsvColor.toColor()
          ..style = PaintingStyle.fill,
      );
    }
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

class _SliderLayout extends MultiChildLayoutDelegate {
  static const String track = 'track';
  static const String thumb = 'thumb';
  static const String gestureContainer = 'gesturecontainer';

  @override
  void performLayout(Size size) {
    layoutChild(
      track,
      BoxConstraints.tightFor(
        width: size.width - 30.0,
        height: size.height / 5,
      ),
    );
    positionChild(track, Offset(15.0, size.height * 0.4));
    layoutChild(
      thumb,
      BoxConstraints.tightFor(width: 5.0, height: size.height / 4),
    );
    positionChild(thumb, Offset(0.0, size.height * 0.4));
    layoutChild(
      gestureContainer,
      BoxConstraints.tightFor(width: size.width, height: size.height),
    );
    positionChild(gestureContainer, Offset.zero);
  }

  @override
  bool shouldRelayout(_SliderLayout oldDelegate) => false;
}

/// Painter for all kinds of track types.
class TrackPainter extends CustomPainter {
  const TrackPainter(this.trackType, this.hsvColor);

  final TrackType trackType;
  final HSVColor hsvColor;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    if (trackType == TrackType.alpha) {
      final Size chessSize = Size(size.height / 2, size.height / 2);
      Paint chessPaintB = Paint()..color = const Color(0xffcccccc);
      Paint chessPaintW = Paint()..color = Colors.white;
      List.generate((size.height / chessSize.height).round(), (int y) {
        List.generate((size.width / chessSize.width).round(), (int x) {
          canvas.drawRect(
            Offset(chessSize.width * x, chessSize.width * y) & chessSize,
            (x + y) % 2 != 0 ? chessPaintW : chessPaintB,
          );
        });
      });
    }

    switch (trackType) {
      case TrackType.hue:
        final List<Color> colors = [
          const HSVColor.fromAHSV(1.0, 0.0, 1.0, 1.0).toColor(),
          const HSVColor.fromAHSV(1.0, 60.0, 1.0, 1.0).toColor(),
          const HSVColor.fromAHSV(1.0, 120.0, 1.0, 1.0).toColor(),
          const HSVColor.fromAHSV(1.0, 180.0, 1.0, 1.0).toColor(),
          const HSVColor.fromAHSV(1.0, 240.0, 1.0, 1.0).toColor(),
          const HSVColor.fromAHSV(1.0, 300.0, 1.0, 1.0).toColor(),
          const HSVColor.fromAHSV(1.0, 360.0, 1.0, 1.0).toColor(),
        ];
        Gradient gradient = LinearGradient(colors: colors);
        canvas.drawRect(rect, Paint()..shader = gradient.createShader(rect));
        break;
      case TrackType.saturation:
        final List<Color> colors = [
          HSVColor.fromAHSV(1.0, hsvColor.hue, 0.0, 1.0).toColor(),
          HSVColor.fromAHSV(1.0, hsvColor.hue, 1.0, 1.0).toColor(),
        ];
        Gradient gradient = LinearGradient(colors: colors);
        canvas.drawRect(rect, Paint()..shader = gradient.createShader(rect));
        break;
      case TrackType.saturationForHSL:
        final List<Color> colors = [
          HSLColor.fromAHSL(1.0, hsvColor.hue, 0.0, 0.5).toColor(),
          HSLColor.fromAHSL(1.0, hsvColor.hue, 1.0, 0.5).toColor(),
        ];
        Gradient gradient = LinearGradient(colors: colors);
        canvas.drawRect(rect, Paint()..shader = gradient.createShader(rect));
        break;
      case TrackType.value:
        final List<Color> colors = [
          HSVColor.fromAHSV(1.0, hsvColor.hue, 1.0, 0.0).toColor(),
          HSVColor.fromAHSV(1.0, hsvColor.hue, 1.0, 1.0).toColor(),
        ];
        Gradient gradient = LinearGradient(colors: colors);
        canvas.drawRect(rect, Paint()..shader = gradient.createShader(rect));
        break;
      case TrackType.lightness:
        final List<Color> colors = [
          HSLColor.fromAHSL(1.0, hsvColor.hue, 1.0, 0.0).toColor(),
          HSLColor.fromAHSL(1.0, hsvColor.hue, 1.0, 0.5).toColor(),
          HSLColor.fromAHSL(1.0, hsvColor.hue, 1.0, 1.0).toColor(),
        ];
        Gradient gradient = LinearGradient(colors: colors);
        canvas.drawRect(rect, Paint()..shader = gradient.createShader(rect));
        break;
      case TrackType.red:
        final List<Color> colors = [
          hsvColor.toColor().withRed(0).withOpacity(1.0),
          hsvColor.toColor().withRed(255).withOpacity(1.0),
        ];
        Gradient gradient = LinearGradient(colors: colors);
        canvas.drawRect(rect, Paint()..shader = gradient.createShader(rect));
        break;
      case TrackType.green:
        final List<Color> colors = [
          hsvColor.toColor().withGreen(0).withOpacity(1.0),
          hsvColor.toColor().withGreen(255).withOpacity(1.0),
        ];
        Gradient gradient = LinearGradient(colors: colors);
        canvas.drawRect(rect, Paint()..shader = gradient.createShader(rect));
        break;
      case TrackType.blue:
        final List<Color> colors = [
          hsvColor.toColor().withBlue(0).withOpacity(1.0),
          hsvColor.toColor().withBlue(255).withOpacity(1.0),
        ];
        Gradient gradient = LinearGradient(colors: colors);
        canvas.drawRect(rect, Paint()..shader = gradient.createShader(rect));
        break;
      case TrackType.alpha:
        final List<Color> colors = [
          hsvColor.toColor().withOpacity(0.0),
          hsvColor.toColor().withOpacity(1.0),
        ];
        Gradient gradient = LinearGradient(colors: colors);
        canvas.drawRect(rect, Paint()..shader = gradient.createShader(rect));
        break;
    }
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for thumb of slider.
class ThumbPainter extends CustomPainter {
  const ThumbPainter({this.thumbColor, this.fullThumbColor = false});

  final Color? thumbColor;
  final bool fullThumbColor;

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawShadow(
      Path()
        ..addOval(
          Rect.fromCircle(center: const Offset(0.5, 2.0), radius: size.width * 1.8),
        ),
      Colors.black,
      3.0,
      true,
    );
    canvas.drawCircle(
        Offset(0.0, size.height * 0.4),
        size.height,
        Paint()
          ..color = Colors.white
          ..style = PaintingStyle.fill);
    if (thumbColor != null) {
      canvas.drawCircle(
          Offset(0.0, size.height * 0.4),
          size.height * (fullThumbColor ? 1.0 : 0.65),
          Paint()
            ..color = thumbColor!
            ..style = PaintingStyle.fill);
    }
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for chess type alpha background in color indicator widget.
class IndicatorPainter extends CustomPainter {
  const IndicatorPainter(this.color);

  final Color color;

  @override
  void paint(Canvas canvas, Size size) {
    final Size chessSize = Size(size.width / 10, size.height / 10);
    final Paint chessPaintB = Paint()..color = const Color(0xFFCCCCCC);
    final Paint chessPaintW = Paint()..color = Colors.white;
    List.generate((size.height / chessSize.height).round(), (int y) {
      List.generate((size.width / chessSize.width).round(), (int x) {
        canvas.drawRect(
          Offset(chessSize.width * x, chessSize.height * y) & chessSize,
          (x + y) % 2 != 0 ? chessPaintW : chessPaintB,
        );
      });
    });

    canvas.drawCircle(
        Offset(size.width / 2, size.height / 2),
        size.height / 2,
        Paint()
          ..color = color
          ..style = PaintingStyle.fill);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Painter for chess type alpha background in slider track widget.
class CheckerPainter extends CustomPainter {
  const CheckerPainter();

  @override
  void paint(Canvas canvas, Size size) {
    final Size chessSize = Size(size.height / 6, size.height / 6);
    Paint chessPaintB = Paint()..color = const Color(0xffcccccc);
    Paint chessPaintW = Paint()..color = Colors.white;
    List.generate((size.height / chessSize.height).round(), (int y) {
      List.generate((size.width / chessSize.width).round(), (int x) {
        canvas.drawRect(
          Offset(chessSize.width * x, chessSize.width * y) & chessSize,
          (x + y) % 2 != 0 ? chessPaintW : chessPaintB,
        );
      });
    });
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}

/// Provide label for color information.
class ColorPickerLabel extends StatefulWidget {
  const ColorPickerLabel(
    this.hsvColor, {
    Key? key,
    this.enableAlpha = true,
    this.colorLabelTypes = const [ColorLabelType.rgb, ColorLabelType.hsv, ColorLabelType.hsl],
    this.textStyle,
  })  : assert(colorLabelTypes.length > 0),
        super(key: key);

  final HSVColor hsvColor;
  final bool enableAlpha;
  final TextStyle? textStyle;
  final List<ColorLabelType> colorLabelTypes;

  @override
  State<ColorPickerLabel> createState() => _ColorPickerLabelState();
}

class _ColorPickerLabelState extends State<ColorPickerLabel> {
  final Map<ColorLabelType, List<String>> _colorTypes = const {
    ColorLabelType.hex: ['R', 'G', 'B', 'A'],
    ColorLabelType.rgb: ['R', 'G', 'B', 'A'],
    ColorLabelType.hsv: ['H', 'S', 'V', 'A'],
    ColorLabelType.hsl: ['H', 'S', 'L', 'A'],
  };

  late ColorLabelType _colorType;

  @override
  void initState() {
    super.initState();
    _colorType = widget.colorLabelTypes[0];
  }

  List<String> colorValue(HSVColor hsvColor, ColorLabelType colorLabelType) {
    if (colorLabelType == ColorLabelType.hex) {
      final Color color = hsvColor.toColor();
      return [
        color.red.toRadixString(16).toUpperCase().padLeft(2, '0'),
        color.green.toRadixString(16).toUpperCase().padLeft(2, '0'),
        color.blue.toRadixString(16).toUpperCase().padLeft(2, '0'),
        color.alpha.toRadixString(16).toUpperCase().padLeft(2, '0'),
      ];
    } else if (colorLabelType == ColorLabelType.rgb) {
      final Color color = hsvColor.toColor();
      return [
        color.red.toString(),
        color.green.toString(),
        color.blue.toString(),
        '${(color.opacity * 100).round()}%',
      ];
    } else if (colorLabelType == ColorLabelType.hsv) {
      return [
        '${hsvColor.hue.round()}°',
        '${(hsvColor.saturation * 100).round()}%',
        '${(hsvColor.value * 100).round()}%',
        '${(hsvColor.alpha * 100).round()}%',
      ];
    } else if (colorLabelType == ColorLabelType.hsl) {
      HSLColor hslColor = hsvToHsl(hsvColor);
      return [
        '${hslColor.hue.round()}°',
        '${(hslColor.saturation * 100).round()}%',
        '${(hslColor.lightness * 100).round()}%',
        '${(hsvColor.alpha * 100).round()}%',
      ];
    } else {
      return ['??', '??', '??', '??'];
    }
  }

  List<Widget> colorValueLabels() {
    double fontSize = 14;
    if (widget.textStyle != null && widget.textStyle?.fontSize != null) fontSize = widget.textStyle?.fontSize ?? 14;

    return [
      for (String item in _colorTypes[_colorType] ?? [])
        if (widget.enableAlpha || item != 'A')
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4.0),
            child: ConstrainedBox(
              constraints: BoxConstraints(minWidth: fontSize * 2),
              child: IntrinsicHeight(
                child: Column(
                  children: <Widget>[
                    Text(
                      item,
                      style: widget.textStyle ?? Theme.of(context).textTheme.bodyLarge,
                    ),
                    const SizedBox(height: 10.0),
                    Expanded(
                      child: Text(
                        colorValue(widget.hsvColor, _colorType)[_colorTypes[_colorType]!.indexOf(item)],
                        overflow: TextOverflow.ellipsis,
                        style: widget.textStyle ?? Theme.of(context).textTheme.bodyMedium,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          )
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Row(mainAxisAlignment: MainAxisAlignment.center, children: <Widget>[
      DropdownButton(
        value: _colorType,
        onChanged: (ColorLabelType? type) {
          if (type != null) setState(() => _colorType = type);
        },
        items: [
          for (ColorLabelType type in widget.colorLabelTypes)
            DropdownMenuItem(
              value: type,
              child: Text(type.toString().split('.').last.toUpperCase()),
            )
        ],
      ),
      const SizedBox(width: 10.0),
      ...colorValueLabels(),
    ]);
  }
}

/// Provide hex input wiget for 3/6/8 digits.
class ColorPickerInput extends StatefulWidget {
  const ColorPickerInput(
    this.color,
    this.onColorChanged, {
    Key? key,
    this.enableAlpha = true,
    this.embeddedText = false,
    this.disable = false,
  }) : super(key: key);

  final Color color;
  final ValueChanged<Color> onColorChanged;
  final bool enableAlpha;
  final bool embeddedText;
  final bool disable;

  @override
  State<ColorPickerInput> createState() => _ColorPickerInputState();
}

class _ColorPickerInputState extends State<ColorPickerInput> {
  TextEditingController textEditingController = TextEditingController();
  int inputColor = 0;

  @override
  void dispose() {
    textEditingController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (inputColor != widget.color.value) {
      // ignore: prefer_interpolation_to_compose_strings
      textEditingController.text = '#' +
          widget.color.red.toRadixString(16).toUpperCase().padLeft(2, '0') +
          widget.color.green.toRadixString(16).toUpperCase().padLeft(2, '0') +
          widget.color.blue.toRadixString(16).toUpperCase().padLeft(2, '0') +
          (widget.enableAlpha ? widget.color.alpha.toRadixString(16).toUpperCase().padLeft(2, '0') : '');
    }
    return Padding(
      padding: const EdgeInsets.only(top: 5.0),
      child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
        if (!widget.embeddedText) Text('Hex', style: Theme.of(context).textTheme.bodyLarge),
        const SizedBox(width: 10),
        SizedBox(
          width: (Theme.of(context).textTheme.bodyMedium?.fontSize ?? 14) * 10,
          child: TextField(
            enabled: !widget.disable,
            controller: textEditingController,
            inputFormatters: [
              UpperCaseTextFormatter(),
              FilteringTextInputFormatter.allow(RegExp(kValidHexPattern)),
            ],
            decoration: InputDecoration(
              isDense: true,
              label: widget.embeddedText ? const Text('Hex') : null,
              contentPadding: const EdgeInsets.symmetric(vertical: 5),
            ),
            onChanged: (String value) {
              String input = value;
              if (value.length == 9) {
                input = value.split('').getRange(7, 9).join() + value.split('').getRange(1, 7).join();
              }
              final Color? color = colorFromHex(input);
              if (color != null) {
                widget.onColorChanged(color);
                inputColor = color.value;
              }
            },
          ),
        ),
      ]),
    );
  }
}

/// 9 track types for slider picker widget.
class ColorPickerSlider extends StatelessWidget {
  const ColorPickerSlider(
    this.trackType,
    this.hsvColor,
    this.onColorChanged, {
    Key? key,
    this.displayThumbColor = false,
    this.fullThumbColor = false,
  }) : super(key: key);

  final TrackType trackType;
  final HSVColor hsvColor;
  final ValueChanged<HSVColor> onColorChanged;
  final bool displayThumbColor;
  final bool fullThumbColor;

  void slideEvent(RenderBox getBox, BoxConstraints box, Offset globalPosition) {
    double localDx = getBox.globalToLocal(globalPosition).dx - 15.0;
    double progress = localDx.clamp(0.0, box.maxWidth - 30.0) / (box.maxWidth - 30.0);
    switch (trackType) {
      case TrackType.hue:
        // 360 is the same as zero
        // if set to 360, sliding to end goes to zero
        onColorChanged(hsvColor.withHue(progress * 359));
        break;
      case TrackType.saturation:
        onColorChanged(hsvColor.withSaturation(progress));
        break;
      case TrackType.saturationForHSL:
        onColorChanged(hslToHsv(hsvToHsl(hsvColor).withSaturation(progress)));
        break;
      case TrackType.value:
        onColorChanged(hsvColor.withValue(progress));
        break;
      case TrackType.lightness:
        onColorChanged(hslToHsv(hsvToHsl(hsvColor).withLightness(progress)));
        break;
      case TrackType.red:
        onColorChanged(HSVColor.fromColor(hsvColor.toColor().withRed((progress * 0xff).round())));
        break;
      case TrackType.green:
        onColorChanged(HSVColor.fromColor(hsvColor.toColor().withGreen((progress * 0xff).round())));
        break;
      case TrackType.blue:
        onColorChanged(HSVColor.fromColor(hsvColor.toColor().withBlue((progress * 0xff).round())));
        break;
      case TrackType.alpha:
        onColorChanged(hsvColor.withAlpha(localDx.clamp(0.0, box.maxWidth - 30.0) / (box.maxWidth - 30.0)));
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (BuildContext context, BoxConstraints box) {
      double thumbOffset = 15.0;
      Color thumbColor;
      switch (trackType) {
        case TrackType.hue:
          thumbOffset += (box.maxWidth - 30.0) * hsvColor.hue / 360;
          thumbColor = HSVColor.fromAHSV(1.0, hsvColor.hue, 1.0, 1.0).toColor();
          break;
        case TrackType.saturation:
          thumbOffset += (box.maxWidth - 30.0) * hsvColor.saturation;
          thumbColor = HSVColor.fromAHSV(1.0, hsvColor.hue, hsvColor.saturation, 1.0).toColor();
          break;
        case TrackType.saturationForHSL:
          thumbOffset += (box.maxWidth - 30.0) * hsvToHsl(hsvColor).saturation;
          thumbColor = HSLColor.fromAHSL(1.0, hsvColor.hue, hsvToHsl(hsvColor).saturation, 0.5).toColor();
          break;
        case TrackType.value:
          thumbOffset += (box.maxWidth - 30.0) * hsvColor.value;
          thumbColor = HSVColor.fromAHSV(1.0, hsvColor.hue, 1.0, hsvColor.value).toColor();
          break;
        case TrackType.lightness:
          thumbOffset += (box.maxWidth - 30.0) * hsvToHsl(hsvColor).lightness;
          thumbColor = HSLColor.fromAHSL(1.0, hsvColor.hue, 1.0, hsvToHsl(hsvColor).lightness).toColor();
          break;
        case TrackType.red:
          thumbOffset += (box.maxWidth - 30.0) * hsvColor.toColor().red / 0xff;
          thumbColor = hsvColor.toColor().withOpacity(1.0);
          break;
        case TrackType.green:
          thumbOffset += (box.maxWidth - 30.0) * hsvColor.toColor().green / 0xff;
          thumbColor = hsvColor.toColor().withOpacity(1.0);
          break;
        case TrackType.blue:
          thumbOffset += (box.maxWidth - 30.0) * hsvColor.toColor().blue / 0xff;
          thumbColor = hsvColor.toColor().withOpacity(1.0);
          break;
        case TrackType.alpha:
          thumbOffset += (box.maxWidth - 30.0) * hsvColor.toColor().opacity;
          thumbColor = hsvColor.toColor().withOpacity(hsvColor.alpha);
          break;
      }

      return CustomMultiChildLayout(
        delegate: _SliderLayout(),
        children: <Widget>[
          LayoutId(
            id: _SliderLayout.track,
            child: ClipRRect(
              borderRadius: const BorderRadius.all(Radius.circular(50.0)),
              child: CustomPaint(
                  painter: TrackPainter(
                trackType,
                hsvColor,
              )),
            ),
          ),
          LayoutId(
            id: _SliderLayout.thumb,
            child: Transform.translate(
              offset: Offset(thumbOffset, 0.0),
              child: CustomPaint(
                painter: ThumbPainter(
                  thumbColor: displayThumbColor ? thumbColor : null,
                  fullThumbColor: fullThumbColor,
                ),
              ),
            ),
          ),
          LayoutId(
            id: _SliderLayout.gestureContainer,
            child: LayoutBuilder(
              builder: (BuildContext context, BoxConstraints box) {
                RenderBox? getBox = context.findRenderObject() as RenderBox?;
                return GestureDetector(
                  onPanDown: (DragDownDetails details) =>
                      getBox != null ? slideEvent(getBox, box, details.globalPosition) : null,
                  onPanUpdate: (DragUpdateDetails details) =>
                      getBox != null ? slideEvent(getBox, box, details.globalPosition) : null,
                );
              },
            ),
          ),
        ],
      );
    });
  }
}

/// Simple round color indicator.
class ColorIndicator extends StatelessWidget {
  const ColorIndicator(
    this.hsvColor, {
    Key? key,
    this.width = 50.0,
    this.height = 50.0,
  }) : super(key: key);

  final HSVColor hsvColor;
  final double width;
  final double height;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      height: height,
      decoration: BoxDecoration(
        borderRadius: const BorderRadius.all(Radius.circular(1000.0)),
        border: Border.all(color: const Color(0xffdddddd)),
      ),
      child: ClipRRect(
        borderRadius: const BorderRadius.all(Radius.circular(1000.0)),
        child: CustomPaint(painter: IndicatorPainter(hsvColor.toColor())),
      ),
    );
  }
}

/// Provide Rectangle & Circle 2 categories, 10 variations of palette widget.
class ColorPickerArea extends StatelessWidget {
  const ColorPickerArea(
    this.hsvColor,
    this.onColorChanged,
    this.paletteType, {
    Key? key,
  }) : super(key: key);

  final HSVColor hsvColor;
  final ValueChanged<HSVColor> onColorChanged;
  final PaletteType paletteType;

  void _handleColorRectChange(double horizontal, double vertical) {
    switch (paletteType) {
      case PaletteType.hsv:
      case PaletteType.hsvWithHue:
        onColorChanged(hsvColor.withSaturation(horizontal).withValue(vertical));
        break;
      case PaletteType.hsvWithSaturation:
        onColorChanged(hsvColor.withHue(horizontal * 360).withValue(vertical));
        break;
      case PaletteType.hsvWithValue:
        onColorChanged(hsvColor.withHue(horizontal * 360).withSaturation(vertical));
        break;
      case PaletteType.hsl:
      case PaletteType.hslWithHue:
        onColorChanged(hslToHsv(
          hsvToHsl(hsvColor).withSaturation(horizontal).withLightness(vertical),
        ));
        break;
      case PaletteType.hslWithSaturation:
        onColorChanged(hslToHsv(
          hsvToHsl(hsvColor).withHue(horizontal * 360).withLightness(vertical),
        ));
        break;
      case PaletteType.hslWithLightness:
        onColorChanged(hslToHsv(
          hsvToHsl(hsvColor).withHue(horizontal * 360).withSaturation(vertical),
        ));
        break;
      case PaletteType.rgbWithRed:
        onColorChanged(HSVColor.fromColor(
          hsvColor.toColor().withBlue((horizontal * 255).round()).withGreen((vertical * 255).round()),
        ));
        break;
      case PaletteType.rgbWithGreen:
        onColorChanged(HSVColor.fromColor(
          hsvColor.toColor().withBlue((horizontal * 255).round()).withRed((vertical * 255).round()),
        ));
        break;
      case PaletteType.rgbWithBlue:
        onColorChanged(HSVColor.fromColor(
          hsvColor.toColor().withRed((horizontal * 255).round()).withGreen((vertical * 255).round()),
        ));
        break;
      default:
        break;
    }
  }

  void _handleColorWheelChange(double hue, double radio) {
    onColorChanged(hsvColor.withHue(hue).withSaturation(radio));
  }

  void _handleGesture(Offset position, BuildContext context, double height, double width) {
    RenderBox? getBox = context.findRenderObject() as RenderBox?;
    if (getBox == null) return;

    Offset localOffset = getBox.globalToLocal(position);
    double horizontal = localOffset.dx.clamp(0.0, width);
    double vertical = localOffset.dy.clamp(0.0, height);

    if (paletteType == PaletteType.hueWheel) {
      Offset center = Offset(width / 2, height / 2);
      double radio = width <= height ? width / 2 : height / 2;
      double dist = sqrt(pow(horizontal - center.dx, 2) + pow(vertical - center.dy, 2)) / radio;
      double rad = (atan2(horizontal - center.dx, vertical - center.dy) / pi + 1) / 2 * 360;
      _handleColorWheelChange(((rad + 90) % 360).clamp(0, 360), dist.clamp(0, 1));
    } else {
      _handleColorRectChange(horizontal / width, 1 - vertical / height);
    }
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        double width = constraints.maxWidth;
        double height = constraints.maxHeight;

        return RawGestureDetector(
          gestures: {
            _AlwaysWinPanGestureRecognizer: GestureRecognizerFactoryWithHandlers<_AlwaysWinPanGestureRecognizer>(
              () => _AlwaysWinPanGestureRecognizer(),
              (_AlwaysWinPanGestureRecognizer instance) {
                instance
                  ..onDown = ((details) => _handleGesture(details.globalPosition, context, height, width))
                  ..onUpdate = ((details) => _handleGesture(details.globalPosition, context, height, width));
              },
            ),
          },
          child: Builder(
            builder: (BuildContext _) {
              switch (paletteType) {
                case PaletteType.hsv:
                case PaletteType.hsvWithHue:
                  return CustomPaint(painter: HSVWithHueColorPainter(hsvColor));
                case PaletteType.hsvWithSaturation:
                  return CustomPaint(painter: HSVWithSaturationColorPainter(hsvColor));
                case PaletteType.hsvWithValue:
                  return CustomPaint(painter: HSVWithValueColorPainter(hsvColor));
                case PaletteType.hsl:
                case PaletteType.hslWithHue:
                  return CustomPaint(painter: HSLWithHueColorPainter(hsvToHsl(hsvColor)));
                case PaletteType.hslWithSaturation:
                  return CustomPaint(painter: HSLWithSaturationColorPainter(hsvToHsl(hsvColor)));
                case PaletteType.hslWithLightness:
                  return CustomPaint(painter: HSLWithLightnessColorPainter(hsvToHsl(hsvColor)));
                case PaletteType.rgbWithRed:
                  return CustomPaint(painter: RGBWithRedColorPainter(hsvColor.toColor()));
                case PaletteType.rgbWithGreen:
                  return CustomPaint(painter: RGBWithGreenColorPainter(hsvColor.toColor()));
                case PaletteType.rgbWithBlue:
                  return CustomPaint(painter: RGBWithBlueColorPainter(hsvColor.toColor()));
                case PaletteType.hueWheel:
                  return CustomPaint(painter: HUEColorWheelPainter(hsvColor));
                default:
                  return const CustomPaint();
              }
            },
          ),
        );
      },
    );
  }
}

/// Provide Hue Ring with HSV Rectangle of palette widget.
class ColorPickerHueRing extends StatelessWidget {
  const ColorPickerHueRing(
    this.hsvColor,
    this.onColorChanged, {
    Key? key,
    this.displayThumbColor = true,
    this.strokeWidth = 5.0,
  }) : super(key: key);

  final HSVColor hsvColor;
  final ValueChanged<HSVColor> onColorChanged;
  final bool displayThumbColor;
  final double strokeWidth;

  void _handleGesture(Offset position, BuildContext context, double height, double width) {
    RenderBox? getBox = context.findRenderObject() as RenderBox?;
    if (getBox == null) return;

    Offset localOffset = getBox.globalToLocal(position);
    double horizontal = localOffset.dx.clamp(0.0, width);
    double vertical = localOffset.dy.clamp(0.0, height);

    Offset center = Offset(width / 2, height / 2);
    double radio = width <= height ? width / 2 : height / 2;
    double dist = sqrt(pow(horizontal - center.dx, 2) + pow(vertical - center.dy, 2)) / radio;
    double rad = (atan2(horizontal - center.dx, vertical - center.dy) / pi + 1) / 2 * 360;
    if (dist > 0.7 && dist < 1.3) onColorChanged(hsvColor.withHue(((rad + 90) % 360).clamp(0, 360)));
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        double width = constraints.maxWidth;
        double height = constraints.maxHeight;

        return RawGestureDetector(
          gestures: {
            _AlwaysWinPanGestureRecognizer: GestureRecognizerFactoryWithHandlers<_AlwaysWinPanGestureRecognizer>(
              () => _AlwaysWinPanGestureRecognizer(),
              (_AlwaysWinPanGestureRecognizer instance) {
                instance
                  ..onDown = ((details) => _handleGesture(details.globalPosition, context, height, width))
                  ..onUpdate = ((details) => _handleGesture(details.globalPosition, context, height, width));
              },
            ),
          },
          child: CustomPaint(
            painter: HueRingPainter(hsvColor, displayThumbColor: displayThumbColor, strokeWidth: strokeWidth),
          ),
        );
      },
    );
  }
}

class _AlwaysWinPanGestureRecognizer extends PanGestureRecognizer {
  @override
  void addAllowedPointer(event) {
    super.addAllowedPointer(event);
    resolve(GestureDisposition.accepted);
  }

  @override
  String get debugDescription => 'alwaysWin';
}

/// Uppercase text formater
class UpperCaseTextFormatter extends TextInputFormatter {
  @override
  TextEditingValue formatEditUpdate(oldValue, TextEditingValue newValue) =>
      TextEditingValue(text: newValue.text.toUpperCase(), selection: newValue.selection);
}
