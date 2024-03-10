import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:rive/rive.dart';

class RiveControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const RiveControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<RiveControl> createState() => _RiveControlState();
}

class _RiveControlState extends State<RiveControl> with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint("Rive build: ${widget.control.id} (${widget.control.hashCode})");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var src = widget.control.attrString("src", "")!;

    if (src == "") {
      return const ErrorControl("Rive must have \"src\" specified.");
    }

    var artBoard = widget.control.attrString("artBoard");
    var antiAliasing = widget.control.attrBool("enableAntiAliasing", true)!;
    var useArtBoardSize = widget.control.attrBool("useArtBoardSize", false)!;
    var fit = parseBoxFit(widget.control, "fit");
    var placeholderCtrls = widget.children.where((c) => c.isVisible);

    return withPageArgs((context, pageArgs) {
      Widget? rive;

      var assetSrc = getAssetSrc(src, pageArgs.pageUri!, pageArgs.assetsDir);
      if (assetSrc.isFile) {
        // Local File
        rive = RiveAnimation.file(
          assetSrc.path,
          artboard: artBoard,
          fit: fit,
          antialiasing: antiAliasing,
          useArtboardSize: useArtBoardSize,
          alignment: parseAlignment(widget.control, "alignment"),
          onInit: (artboard) {
            widget.backend.triggerControlEvent(widget.control.id, "init");
          },
          placeHolder: placeholderCtrls.isNotEmpty
              ? createControl(
                  widget.control, placeholderCtrls.first.id, disabled,
                  parentAdaptive: widget.parentAdaptive)
              : null,
        );
      } else {
        // URL
        rive = RiveAnimation.network(
          assetSrc.path,
          artboard: artBoard,
          fit: fit,
          antialiasing: antiAliasing,
          useArtboardSize: useArtBoardSize,
          alignment: parseAlignment(widget.control, "alignment"),
          onInit: (artboard) {
            widget.backend.triggerControlEvent(widget.control.id, "init");
          },
          placeHolder: placeholderCtrls.isNotEmpty
              ? createControl(
                  widget.control, placeholderCtrls.first.id, disabled)
              : null,
        );
      }

      return constrainedControl(context, rive, widget.parent, widget.control);
    });
  }
}
