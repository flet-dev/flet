import 'package:flutter/material.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import 'create_control.dart';
import 'error.dart';

class BottomSheetControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final dynamic dispatch;
  final Widget? nextChild;

  const BottomSheetControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.dispatch,
      required this.nextChild})
      : super(key: key);

  @override
  State<BottomSheetControl> createState() => _BottomSheetControlState();
}

class _BottomSheetControlState extends State<BottomSheetControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("BottomSheet build: ${widget.control.id}");

    var server = FletAppServices.of(context).server;

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
      List<Map<String, String>> props = [
        {"i": widget.control.id, "open": "false"}
      ];
      widget.dispatch(
          UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
      server.updateControlProps(props: props);
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
                      widget.control, contentCtrls.first.id, disabled);

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
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "dismiss",
                eventData: "");
          }
        });
      });
    } else if (open != lastOpen && lastOpen) {
      Navigator.pop(context);
    }

    return const SizedBox.shrink();
  }
}
