import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:rive/rive.dart';

class RiveControl extends StatefulWidget {
  final Control control;

  const RiveControl({super.key, required this.control});

  @override
  State<RiveControl> createState() => _RiveControlState();
}

class _RiveControlState extends State<RiveControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("Rive build: ${widget.control.id} (${widget.control.hashCode})");
    var src = widget.control.getString("src");
    if (src == null) {
      return const ErrorControl("Rive must have \"src\" specified.");
    }

    var artBoard = widget.control.getString("art_board");
    var antiAliasing = widget.control.getBool("enable_anti_aliasing", true)!;
    var useArtBoardSize = widget.control.getBool("use_art_board_size", false)!;
    var fit = widget.control.getBoxFit("fit");
    var alignment = widget.control.getAlignment("alignment");
    var placeholder = widget.control.buildWidget("placeholder");
    var speedMultiplier = widget.control.getDouble("speed_multiplier", 1)!;
    var animations = widget.control.get<List<String>>("animations", const [])!;
    var stateMachines =
        widget.control.get<List<String>>("state_machines", const [])!;
    var headers = widget.control.get("headers")?.cast<String, String>();
    var clipRect = widget.control.getRect("clip_rect");

    Widget? rive;

    var assetSrc = widget.control.backend.getAssetSource(src);
    if (assetSrc.isFile) {
      // Local File
      rive = RiveAnimation.file(
        assetSrc.path,
        artboard: artBoard,
        fit: fit,
        antialiasing: antiAliasing,
        useArtboardSize: useArtBoardSize,
        alignment: alignment,
        placeHolder: placeholder,
        speedMultiplier: speedMultiplier,
        animations: animations,
        stateMachines: stateMachines,
        clipRect: clipRect,
      );
    } else {
      // URL
      rive = RiveAnimation.network(
        assetSrc.path,
        fit: fit,
        artboard: artBoard,
        alignment: alignment,
        antialiasing: antiAliasing,
        useArtboardSize: useArtBoardSize,
        placeHolder: placeholder,
        speedMultiplier: speedMultiplier,
        animations: animations,
        stateMachines: stateMachines,
        headers: headers,
        clipRect: clipRect,
        // onInit: _onInit,
      );
    }

    return ConstrainedControl(control: widget.control, child: rive);
  }
}
