import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_control_stateful_mixin.dart';

class ChipControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const ChipControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  State<ChipControl> createState() => _ChipControlState();
}

class _ChipControlState extends State<ChipControl>
    with FletControlStatefulMixin {
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
    var strSelected = selected.toString();
    debugPrint(strSelected);
    _selected = selected;
    updateControlProps(widget.control.id, {"selected": strSelected});
    sendControlEvent(widget.control.id, "select", strSelected);
  }

  void _onFocusChange() {
    sendControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur", "");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Chip build: ${widget.control.id}");

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
    var deleteIconColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("deleteIconColor", "")!);
    var disabledColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("disabledColor", "")!);

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
    bool showCheckmark = widget.control.attrBool("showCheckmark", true)!;
    String deleteButtonTooltipMessage =
        widget.control.attrString("deleteButtonTooltipMessage", "")!;

    var elevation = widget.control.attrDouble("elevation");

    Function()? onClickHandler = onClick && !disabled
        ? () {
            debugPrint("Chip ${widget.control.id} clicked!");
            sendControlEvent(widget.control.id, "click", "");
          }
        : null;

    Function()? onDeleteHandler = onDelete && !disabled
        ? () {
            debugPrint("Chip ${widget.control.id} deleted!");
            sendControlEvent(widget.control.id, "delete", "");
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
          showCheckmark: showCheckmark,
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
          deleteIconColor: deleteIconColor,
          disabledColor: disabledColor,
          elevation: elevation,
          isEnabled: !disabled,
          padding: parseEdgeInsets(widget.control, "padding"),
          labelPadding: parseEdgeInsets(widget.control, "labelPadding"),
          labelStyle:
              parseTextStyle(Theme.of(context), widget.control, "labelStyle"),
          selectedColor: HexColor.fromString(Theme.of(context),
              widget.control.attrString("selectedColor", "")!),
          selectedShadowColor: HexColor.fromString(Theme.of(context),
              widget.control.attrString("selectedShadowColor", "")!),
          shadowColor: HexColor.fromString(
              Theme.of(context), widget.control.attrString("shadowColor", "")!),
          shape: parseOutlinedBorder(widget.control, "shape"),
        ),
        widget.parent,
        widget.control);
  }
}
