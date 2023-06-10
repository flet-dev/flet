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
  bool _open = false;

  Widget _createBottomSheet() {
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var contentCtrls = widget.children.where((c) => c.name == "content");

    if (contentCtrls.isEmpty) {
      return const ErrorControl("BottomSheet does not have a content.");
    }

    return createControl(widget.control, contentCtrls.first.id, disabled);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("BottomSheet build: ${widget.control.id}");

    var open = widget.control.attrBool("open", false)!;
    //var modal = widget.control.attrBool("modal", true)!;
    var dismissible = widget.control.attrBool("dismissible", true)!;
    var enableDrag = widget.control.attrBool("enableDrag", false)!;
    var showDragHandle = widget.control.attrBool("showDragHandle", false)!;
    var useSafeArea = widget.control.attrBool("useSafeArea", true)!;

    void resetOpenState() {
      List<Map<String, String>> props = [
        {"i": widget.control.id, "open": "false"}
      ];
      widget.dispatch(
          UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
      FletAppServices.of(context).server.updateControlProps(props: props);
    }

    if (!open && _open) {
      _open = false;
      resetOpenState();
      Navigator.pop(context);
    } else if (open && !_open) {
      var bottomSheet = _createBottomSheet();
      if (bottomSheet is ErrorControl) {
        return bottomSheet;
      }

      _open = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showModalBottomSheet<void>(
                context: context,
                builder: (context) {
                  return bottomSheet;
                },
                isDismissible: dismissible,
                enableDrag: enableDrag,
                showDragHandle: showDragHandle,
                useSafeArea: useSafeArea)
            .then((value) {
          debugPrint("BottomSheet dismissed: $_open");
          bool shouldDismiss = _open;
          _open = false;

          if (shouldDismiss) {
            resetOpenState();
            FletAppServices.of(context).server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "dismiss",
                eventData: "");
          }
        });
      });
    }

    return widget.nextChild ?? const SizedBox.shrink();
  }
}
