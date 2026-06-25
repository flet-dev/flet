import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';

import 'boot_screen.dart';
import 'spinkit.dart';

class Extension extends FletExtension {
  @override
  Widget? createBootScreen(String name, Map<String, dynamic> options,
      ValueListenable<BootStatus> status) {
    return name == "spinkit"
        ? SpinKitBootScreen(options: options, status: status)
        : null;
  }

  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "SpinKitRotatingPlain":
      case "SpinKitDoubleBounce":
      case "SpinKitWave":
      case "SpinKitWanderingCubes":
      case "SpinKitFadingFour":
      case "SpinKitFadingCube":
      case "SpinKitPulse":
      case "SpinKitChasingDots":
      case "SpinKitThreeBounce":
      case "SpinKitCircle":
      case "SpinKitCubeGrid":
      case "SpinKitFadingCircle":
      case "SpinKitRotatingCircle":
      case "SpinKitFoldingCube":
      case "SpinKitPumpingHeart":
      case "SpinKitHourGlass":
      case "SpinKitPouringHourGlass":
      case "SpinKitPouringHourGlassRefined":
      case "SpinKitFadingGrid":
      case "SpinKitRing":
      case "SpinKitRipple":
      case "SpinKitDualRing":
      case "SpinKitSpinningCircle":
      case "SpinKitSpinningLines":
      case "SpinKitSquareCircle":
      case "SpinKitThreeInOut":
      case "SpinKitDancingSquare":
      case "SpinKitPianoWave":
      case "SpinKitPulsingGrid":
      case "SpinKitWaveSpinner":
        return SpinKitControl(key: key, control: control);
      default:
        return null;
    }
  }
}
