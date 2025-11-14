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

class BottomSheetControl extends StatelessWidget {
  final Control control;

  BottomSheetControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  Widget build(BuildContext context) {
    debugPrint("BottomSheet build: ${control.id}");

    bool lastOpen = control.getBool("_open", false)!;
    var open = control.getBool("open", false)!;

    var maintainBottomViewInsetsPadding =
        control.getBool("maintain_bottom_view_insets_padding", true)!;
    final fullscreen = control.getBool("fullscreen", false)!;
    final scrollable = fullscreen || control.getBool("scrollable", false)!;
    final draggable = control.getBool("draggable", false)!;

    if (open && !lastOpen) {
      control.updateProperties({"_open": open}, python: false);

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showModalBottomSheet<void>(
                context: context,
                builder: (context) {
                  var content = control.buildWidget("content");

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

                  if (fullscreen) {
                    content = SizedBox.expand(child: content);
                  }

                  return content;
                },
                isDismissible: control.getBool("dismissible", true)!,
                backgroundColor: control.getColor("bgcolor", context),
                elevation: control.getDouble("elevation"),
                isScrollControlled: scrollable,
                enableDrag: draggable,
                barrierColor: control.getColor("barrier_color", context),
                sheetAnimationStyle:
                    control.getAnimationStyle("animation_style"),
                constraints: fullscreen
                    ? null
                    : control.getBoxConstraints("size_constraints"),
                showDragHandle: control.getBool("show_drag_handle", false)!,
                clipBehavior: control.getClipBehavior("clip_behavior"),
                shape: control.getOutlinedBorder("shape", Theme.of(context)),
                useSafeArea: control.getBool("use_safe_area", true)!)
            .then((value) {
          control.updateProperties({"_open": false}, python: false);
          control.updateProperties({"open": false});
          control.triggerEvent("dismiss");
        });
      });
    } else if (open != lastOpen && lastOpen) {
      Navigator.of(context).pop();
    }

    return const SizedBox.shrink();
  }
}
