import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class SpinKitControl extends StatefulWidget {
  final Control control;

  const SpinKitControl({super.key, required this.control});

  @override
  State<SpinKitControl> createState() => _SpinKitControlState();
}

class _SpinKitControlState extends State<SpinKitControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("SpinKitControl build: ${widget.control.id} (${widget.control.type})");

    final color =
        widget.control.getColor("color", context) ?? Theme.of(context).primaryColor;
    final size = widget.control.getDouble("size", 50.0)!;
    final duration = widget.control.getDuration("duration");

    final lineWidth = widget.control.getDouble("line_width");
    final borderWidth = widget.control.getDouble("border_width");
    final itemCount = widget.control.getInt("item_count");
    final waveType = parseEnum(SpinKitWaveType.values,
        widget.control.getString("wave_type"), SpinKitWaveType.start)!;

    final spinner = createSpinKit(
      widget.control.type,
      color: color,
      size: size,
      duration: duration,
      lineWidth: lineWidth,
      borderWidth: borderWidth,
      itemCount: itemCount,
      waveType: waveType,
    );

    return LayoutControl(control: widget.control, child: spinner);
  }
}

/// Builds a `flutter_spinkit` spinner widget for the given [type] (a
/// `SpinKit…` control type string).
///
/// Shared by [SpinKitControl] and the SpinKit boot screen. Falls back to
/// [SpinKitRotatingCircle] for unknown types. Per-spinner defaults match the
/// `flutter_spinkit` recommendations.
Widget createSpinKit(
  String type, {
  required Color color,
  required double size,
  Duration? duration,
  double? lineWidth,
  double? borderWidth,
  int? itemCount,
  SpinKitWaveType waveType = SpinKitWaveType.start,
}) {
  switch (type) {
    case "SpinKitRotatingPlain":
      return SpinKitRotatingPlain(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    case "SpinKitDoubleBounce":
      return SpinKitDoubleBounce(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 2000),
      );
    case "SpinKitWave":
      return SpinKitWave(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
        itemCount: itemCount ?? 5,
        type: waveType,
      );
    case "SpinKitWanderingCubes":
      return SpinKitWanderingCubes(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1800),
      );
    case "SpinKitFadingFour":
      return SpinKitFadingFour(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    case "SpinKitFadingCube":
      return SpinKitFadingCube(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    case "SpinKitPulse":
      return SpinKitPulse(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1000),
      );
    case "SpinKitChasingDots":
      return SpinKitChasingDots(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 2000),
      );
    case "SpinKitThreeBounce":
      return SpinKitThreeBounce(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1400),
      );
    case "SpinKitCircle":
      return SpinKitCircle(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    case "SpinKitCubeGrid":
      return SpinKitCubeGrid(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    case "SpinKitFadingCircle":
      return SpinKitFadingCircle(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    case "SpinKitRotatingCircle":
      return SpinKitRotatingCircle(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    case "SpinKitFoldingCube":
      return SpinKitFoldingCube(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 2400),
      );
    case "SpinKitPumpingHeart":
      return SpinKitPumpingHeart(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1000),
      );
    case "SpinKitHourGlass":
      return SpinKitHourGlass(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    case "SpinKitPouringHourGlass":
      return SpinKitPouringHourGlass(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 2400),
      );
    case "SpinKitPouringHourGlassRefined":
      return SpinKitPouringHourGlassRefined(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 2400),
      );
    case "SpinKitFadingGrid":
      return SpinKitFadingGrid(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    case "SpinKitRing":
      return SpinKitRing(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
        lineWidth: lineWidth ?? 7.0,
      );
    case "SpinKitRipple":
      return SpinKitRipple(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1800),
        borderWidth: borderWidth ?? 6.0,
      );
    case "SpinKitDualRing":
      return SpinKitDualRing(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
        lineWidth: lineWidth ?? 7.0,
      );
    case "SpinKitSpinningCircle":
      return SpinKitSpinningCircle(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    case "SpinKitSpinningLines":
      return SpinKitSpinningLines(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
        lineWidth: lineWidth ?? 2.0,
      );
    case "SpinKitSquareCircle":
      return SpinKitSquareCircle(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 500),
      );
    case "SpinKitThreeInOut":
      return SpinKitThreeInOut(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1500),
      );
    case "SpinKitDancingSquare":
      return SpinKitDancingSquare(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    case "SpinKitPianoWave":
      return SpinKitPianoWave(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
        itemCount: itemCount ?? 5,
      );
    case "SpinKitPulsingGrid":
      return SpinKitPulsingGrid(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    case "SpinKitWaveSpinner":
      return SpinKitWaveSpinner(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
    default:
      return SpinKitRotatingCircle(
        color: color,
        size: size,
        duration: duration ?? const Duration(milliseconds: 1200),
      );
  }
}
