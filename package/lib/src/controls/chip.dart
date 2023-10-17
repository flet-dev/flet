import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
//import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';
import 'package:flet/src/flet_app_services.dart';
import '../actions.dart';
import '../protocol/update_control_props_payload.dart';

class ChipControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final dynamic dispatch;

  const ChipControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.dispatch})
      : super(key: key);

  @override
  State<ChipControl> createState() => _ChipControlState();
}

class _ChipControlState extends State<ChipControl> {
  bool _selected = false;

  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _onSelect(bool selected) {
    var sselected = selected.toString();
    debugPrint(sselected);
    setState(() {
      _selected = selected;
    });
    List<Map<String, String>> props = [
      {"i": widget.control.id, "selected": sselected}
    ];
    widget.dispatch(
        UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
    final server = FletAppServices.of(context).server;
    server.updateControlProps(props: props);
    server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: "select",
        eventData: sselected);
  }

  void _onFocusChange() {
    FletAppServices.of(context).server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: _focusNode.hasFocus ? "focus" : "blur",
        eventData: "");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Chip build: ${widget.control.id}");

    // var contentCtrls =
    //     children.where((c) => c.name == "content" && c.isVisible);
    var labelCtrls =
        widget.children.where((c) => c.name == "label" && c.isVisible);
    var leadingCtrls =
        widget.children.where((c) => c.name == "leading" && c.isVisible);
    var deleteIconCtrls =
        widget.children.where((c) => c.name == "deleteIcon" && c.isVisible);

    if (labelCtrls.isEmpty) {
      return const ErrorControl("Chip must have label specified.");
    }

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var bgcolor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("bgcolor", "")!);

    final server = FletAppServices.of(context).server;
    bool onClick = widget.control.attrBool("onclick", false)!;
    bool onDelete = widget.control.attrBool("onDelete", false)!;
    bool onSelect = widget.control.attrBool("onSelect", false)!;

    if (onSelect && onClick) {
      return const ErrorControl(
          "Chip cannot have both on_select and on_click events specified.");
    }

    bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool selected = widget.control.attrBool("selected", false)!;
    if (_selected != selected) {
      _selected = selected;
    }

    String deleteButtonTooltipMessage =
        widget.control.attrString("deleteButtonTooltipMessage", "")!;

    Function()? onClickHandler = onClick && !disabled
        ? () {
            debugPrint("Chip ${widget.control.id} clicked!");
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "click",
                eventData: "");
          }
        : null;

    Function()? onDeleteHandler = onDelete && !disabled
        ? () {
            debugPrint("Chip ${widget.control.id} deleted!");
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "delete",
                eventData: "");
          }
        : null;

    return constrainedControl(
        context,
        InputChip(
          autofocus: autofocus,
          focusNode: _focusNode,
          label: createControl(widget.control, labelCtrls.first.id, disabled),
          avatar: leadingCtrls.isNotEmpty
              ? createControl(widget.control, leadingCtrls.first.id, disabled)
              : null,
          backgroundColor: bgcolor,
          checkmarkColor: HexColor.fromString(
              Theme.of(context), widget.control.attrString("checkColor", "")!),
          selected: _selected,
          deleteButtonTooltipMessage: deleteButtonTooltipMessage,
          onPressed: onClickHandler,
          onDeleted: onDeleteHandler,
          onSelected: onSelect && !disabled
              ? (bool selected) {
                  _onSelect(selected);
                }
              : null,
          deleteIcon: deleteIconCtrls.isNotEmpty
              ? createControl(
                  widget.control, deleteIconCtrls.first.id, disabled)
              : null,
        ),

        // deleteIcon: const Icon(
        //   Icons.cancel,
        // ),

        widget.parent,
        widget.control);
  }
}
