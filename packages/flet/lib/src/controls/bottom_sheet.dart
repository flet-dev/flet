import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
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
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var open = widget.control.attrBool("open", false)!;
    //var modal = widget.control.attrBool("modal", true)!;
    var dismissible = widget.control.attrBool("dismissible", true)!;
    var enableDrag = widget.control.attrBool("enableDrag", false)!;
    var showDragHandle = widget.control.attrBool("showDragHandle", false)!;
    var useSafeArea = widget.control.attrBool("useSafeArea", true)!;
    var isScrollControlled =
        widget.control.attrBool("isScrollControlled", false)!;
    var maintainBottomViewInsetsPadding =
        widget.control.attrBool("maintainBottomViewInsetsPadding", true)!;

    void resetOpenState() {
      widget.backend.updateControlState(widget.control.id, {"open": "false"});
    }

    if (open && !lastOpen) {
      widget.control.state["open"] = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showModalBottomSheet<void>(
                context: context,
                builder: (context) {
                  var contentCtrls =
                      widget.children.where((c) => c.name == "content");

                  if (contentCtrls.isEmpty) {
                    return const ErrorControl(
                        "BottomSheet does not have a content.");
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
                backgroundColor: widget.control.attrColor("bgColor", context),
                elevation: widget.control.attrDouble("elevation"),
                isScrollControlled: isScrollControlled,
                enableDrag: enableDrag,
                showDragHandle: showDragHandle,
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
