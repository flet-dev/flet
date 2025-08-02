import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/colors.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';

class BottomSheetControl extends StatefulWidget {
  final Control control;

  BottomSheetControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<BottomSheetControl> createState() => _BottomSheetControlState();
}

class _BottomSheetControlState extends State<BottomSheetControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("BottomSheet build: ${widget.control.id}");

    bool lastOpen = widget.control.getBool("_open", false)!;
    var open = widget.control.getBool("open", false)!;

    var maintainBottomViewInsetsPadding =
        widget.control.getBool("maintain_bottom_view_insets_padding", true)!;

    if (open && !lastOpen) {
      widget.control.updateProperties({"_open": open}, python: false);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showModalBottomSheet<void>(
                context: context,
                builder: (context) {
                  var content = widget.control.buildWidget("content");

                  if (content == null) {
                    return const ErrorControl(
                        "BottomSheet.content must be visible");
                  }

                  if (maintainBottomViewInsetsPadding) {
                    content = Padding(
                      padding: EdgeInsets.only(
                          bottom: MediaQuery.of(context).viewInsets.bottom),
                      child: content,
                    );
                  }

                  return content;
                },
                isDismissible: widget.control.getBool("dismissible", true)!,
                backgroundColor: widget.control.getColor("bgcolor", context),
                elevation: widget.control.getDouble("elevation"),
                isScrollControlled:
                    widget.control.getBool("scroll_controlled", false)!,
                enableDrag: widget.control.getBool("enable_drag", false)!,
                barrierColor: widget.control.getColor("barrier_color", context),
                sheetAnimationStyle:
                    widget.control.getAnimationStyle("animation_style"),
                constraints:
                    widget.control.getBoxConstraints("size_constraints"),
                showDragHandle:
                    widget.control.getBool("show_drag_handle", false)!,
                clipBehavior: widget.control.getClipBehavior("clip_behavior"),
                shape: widget.control
                    .getOutlinedBorder("shape", Theme.of(context)),
                useSafeArea: widget.control.getBool("use_safe_area", true)!)
            .then((value) {
          widget.control.updateProperties({"_open": false}, python: false);
          widget.control.updateProperties({"open": false});
          widget.control.triggerEvent("dismiss");
        });
      });
    } else if (open != lastOpen && lastOpen) {
      Navigator.of(context).pop();
    }

    return const SizedBox.shrink();
  }
}
