import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
import '../utils/text.dart';
import '../utils/theme.dart';
import 'create_control.dart';
import 'error.dart';

class ChipControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const ChipControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

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
    var strSelected = selected.toString();
    debugPrint(strSelected);
    _selected = selected;
    widget.backend
        .updateControlState(widget.control.id, {"selected": strSelected});
    widget.backend
        .triggerControlEvent(widget.control.id, "select", strSelected);
  }

  void _onFocusChange() {
    widget.backend.triggerControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Chip build: ${widget.control.id}");
    bool disabled = widget.control.disabled || widget.parentDisabled;

    var labelCtrls =
        widget.children.where((c) => c.name == "label" && c.visible);
    if (labelCtrls.isEmpty) {
      return const ErrorControl("Chip.label must be provided and visible");
    }
    var leadingCtrls =
        widget.children.where((c) => c.name == "leading" && c.visible);
    var deleteIconCtrls =
        widget.children.where((c) => c.name == "deleteIcon" && c.visible);

    var onClick = widget.control.getBool("onclick", false)!;
    var onDelete = widget.control.getBool("onDelete", false)!;
    var onSelect = widget.control.getBool("onSelect", false)!;

    if (onSelect && onClick) {
      return const ErrorControl(
          "Chip cannot have both on_select and on_click events specified");
    }

    bool selected = widget.control.getBool("selected", false)!;
    if (_selected != selected) {
      _selected = selected;
    }

    return constrainedControl(
        context,
        InputChip(
          autofocus: widget.control.getBool("autofocus", false)!,
          focusNode: _focusNode,
          label: createControl(widget.control, labelCtrls.first.id, disabled,
              parentAdaptive: widget.parentAdaptive),
          avatar: leadingCtrls.isNotEmpty
              ? createControl(widget.control, leadingCtrls.first.id, disabled,
                  parentAdaptive: widget.parentAdaptive)
              : null,
          backgroundColor: widget.control.getColor("bgcolor", context),
          checkmarkColor: widget.control.getColor("checkColor", context),
          selected: _selected,
          showCheckmark: widget.control.getBool("showCheckmark", true)!,
          deleteButtonTooltipMessage:
              widget.control.getString("deleteButtonTooltip"),
          deleteIcon: deleteIconCtrls.isNotEmpty
              ? createControl(
                  widget.control, deleteIconCtrls.first.id, disabled,
                  parentAdaptive: widget.parentAdaptive)
              : null,
          deleteIconColor: widget.control.getColor("deleteIconColor", context),
          disabledColor: widget.control.getColor("disabledColor", context),
          elevation: widget.control.getDouble("elevation"),
          isEnabled: !disabled,
          padding: parseEdgeInsets(widget.control, "padding"),
          labelPadding: parseEdgeInsets(widget.control, "labelPadding"),
          labelStyle:
              parseTextStyle(Theme.of(context), widget.control, "labelStyle"),
          selectedColor: widget.control.getColor("selectedColor", context),
          selectedShadowColor:
              widget.control.getColor("selectedShadowColor", context),
          shadowColor: widget.control.getColor("shadowColor", context),
          shape: parseOutlinedBorder(widget.control, "shape"),
          color:
              parseWidgetStateColor(Theme.of(context), widget.control, "color"),
          surfaceTintColor:
              widget.control.getColor("surfaceTintColor", context),
          pressElevation: widget.control.getDouble("clickElevation"),
          side:
              parseBorderSide(Theme.of(context), widget.control, "borderSide"),
          clipBehavior:
              parseClip(widget.control.getString("clipBehavior"), Clip.none)!,
          visualDensity:
              parseVisualDensity(widget.control.getString("visualDensity")),
          avatarBoxConstraints:
              parseBoxConstraints(widget.control, "leadingSizeConstraints"),
          deleteIconBoxConstraints:
              parseBoxConstraints(widget.control, "deleteIconSizeConstraints"),
          chipAnimationStyle: ChipAnimationStyle(
            enableAnimation:
                parseAnimationStyle(widget.control, "enableAnimationStyle"),
            selectAnimation:
                parseAnimationStyle(widget.control, "selectAnimationStyle"),
            avatarDrawerAnimation: parseAnimationStyle(
                widget.control, "leadingDrawerAnimationStyle"),
            deleteDrawerAnimation: parseAnimationStyle(
                widget.control, "deleteDrawerAnimationStyle"),
          ),
          onPressed: onClick && !disabled
              ? () {
                  widget.backend
                      .triggerControlEvent(widget.control.id, "click");
                }
              : null,
          onDeleted: onDelete && !disabled
              ? () {
                  widget.backend
                      .triggerControlEvent(widget.control.id, "delete");
                }
              : null,
          onSelected: onSelect && !disabled
              ? (bool selected) {
                  _onSelect(selected);
                }
              : null,
        ),
        widget.parent,
        widget.control);
  }
}
