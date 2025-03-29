import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/others.dart';
import 'create_control.dart';
import 'error.dart';

class BottomSheetControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final Widget? nextChild;
  final FletControlBackend backend;

  const BottomSheetControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.nextChild,
      required this.backend});

  @override
  State<BottomSheetControl> createState() => _BottomSheetControlState();
}

class _BottomSheetControlState extends State<BottomSheetControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("BottomSheet build: ${widget.control.id}");

    bool lastOpen = widget.control.state["open"] ?? false;
    bool disabled = widget.control.disabled || widget.parentDisabled;

    var open = widget.control.getBool("open", false)!;
    //var modal = widget.control.attrBool("modal", true)!;
    var dismissible = widget.control.getBool("dismissible", true)!;
    var enableDrag = widget.control.getBool("enableDrag", false)!;
    var showDragHandle = widget.control.getBool("showDragHandle", false)!;
    var useSafeArea = widget.control.getBool("useSafeArea", true)!;
    var isScrollControlled =
        widget.control.getBool("isScrollControlled", false)!;
    var maintainBottomViewInsetsPadding =
        widget.control.getBool("maintainBottomViewInsetsPadding", true)!;

    void resetOpenState() {
      widget.backend.updateControlState(widget.control.id, {"open": "false"});
    }

    if (open && !lastOpen) {
      widget.control.state["open"] = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showModalBottomSheet<void>(
                context: context,
                builder: (context) {
                  var contentCtrls = widget.children
                      .where((c) => c.name == "content" && c.visible);

                  if (contentCtrls.isEmpty) {
                    return const ErrorControl(
                        "BottomSheet.content must be provided and visible");
                  }

                  var content = createControl(
                      widget.control, contentCtrls.first.id, disabled,
                      parentAdaptive: widget.parentAdaptive);

                  if (content is ErrorControl) {
                    return content;
                  }

                  if (maintainBottomViewInsetsPadding) {
                    var bottomPadding =
                        MediaQuery.of(context).viewInsets.bottom;
                    debugPrint("bottomPadding: $bottomPadding");
                    content = Padding(
                      padding: EdgeInsets.only(
                          bottom: MediaQuery.of(context).viewInsets.bottom),
                      child: content,
                    );
                  }

                  return content;
                },
                isDismissible: dismissible,
                backgroundColor: widget.control.getColor("bgColor", context),
                elevation: widget.control.getDouble("elevation"),
                isScrollControlled: isScrollControlled,
                enableDrag: enableDrag,
                barrierColor: widget.control.getColor("barrierColor", context),
                sheetAnimationStyle:
                    parseAnimationStyle(widget.control, "animationStyle"),
                constraints:
                    parseBoxConstraints(widget.control, "sizeConstraints"),
                showDragHandle: showDragHandle,
                clipBehavior:
                    parseClip(widget.control.getString("clipBehavior")),
                shape: parseOutlinedBorder(widget.control, "shape"),
                useSafeArea: useSafeArea)
            .then((value) {
          lastOpen = widget.control.state["open"] ?? false;
          debugPrint("BottomSheet dismissed: $lastOpen");
          bool shouldDismiss = lastOpen;
          widget.control.state["open"] = false;

          if (shouldDismiss) {
            resetOpenState();
            widget.backend.triggerControlEvent(widget.control.id, "dismiss");
          }
        });
      });
    } else if (open != lastOpen && lastOpen) {
      Navigator.of(context).pop();
    }

    return const SizedBox.shrink();
  }
}
