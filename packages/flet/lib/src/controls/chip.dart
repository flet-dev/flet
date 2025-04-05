import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
import '../utils/text.dart';
import '../utils/theme.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class ChipControl extends StatefulWidget {
  final Control control;

  const ChipControl({super.key, required this.control});

  @override
  State<ChipControl> createState() => _ChipControlState();
}

class _ChipControlState extends State<ChipControl> {
  bool _selected = false;
  late final FocusNode _focusNode;
  late final FletBackend backend;

  @override
  void initState() {
    super.initState();
    backend = FletBackend.of(context);
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _onFocusChange() {
    backend.triggerControlEvent(
        widget.control, _focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Chip build: ${widget.control.id}");
    bool disabled = widget.control.disabled;

    var label = widget.control.buildWidget("label");
    if (label == null) {
      return const ErrorControl("Chip.label must be provided and visible");
    }

    var onClick = widget.control.getBool("on_click", false)!;
    var onDelete = widget.control.getBool("on_delete", false)!;
    var onSelect = widget.control.getBool("on_select", false)!;
    if (onSelect && onClick) {
      return const ErrorControl(
          "Chip cannot have both on_select and on_click events specified");
    }

    bool selected = widget.control.getBool("selected", false)!;
    if (_selected != selected) {
      _selected = selected;
    }

    final chip = InputChip(
      autofocus: widget.control.getBool("autofocus", false)!,
      focusNode: _focusNode,
      label: label,
      avatar: widget.control.buildWidget("leading"),
      backgroundColor: widget.control.getColor("bgcolor", context),
      checkmarkColor: widget.control.getColor("check_color", context),
      selected: _selected,
      showCheckmark: widget.control.getBool("show_checkmark", true)!,
      deleteButtonTooltipMessage:
          widget.control.getString("delete_button_tooltip"),
      deleteIcon: widget.control.buildWidget("delete_icon"),
      deleteIconColor: widget.control.getColor("delete_icon_color", context),
      disabledColor: widget.control.getColor("disabled_color", context),
      elevation: widget.control.getDouble("elevation"),
      isEnabled: !disabled,
      padding: parseEdgeInsets(widget.control, "padding"),
      labelPadding: parseEdgeInsets(widget.control, "label_padding"),
      labelStyle:
          parseTextStyle(Theme.of(context), widget.control, "label_style"),
      selectedColor: widget.control.getColor("selected_color", context),
      selectedShadowColor:
          widget.control.getColor("selected_shadow_color", context),
      shadowColor: widget.control.getColor("shadow_color", context),
      shape: parseOutlinedBorder(widget.control, "shape"),
      color: parseWidgetStateColor(Theme.of(context), widget.control, "color"),
      surfaceTintColor: widget.control.getColor("surface_tint_color", context),
      pressElevation: widget.control.getDouble("click_elevation"),
      side: parseBorderSide(Theme.of(context), widget.control, "border_side"),
      clipBehavior:
          parseClip(widget.control.getString("clip_behavior"), Clip.none)!,
      visualDensity:
          parseVisualDensity(widget.control.getString("visual_density")),
      avatarBoxConstraints:
          parseBoxConstraints(widget.control, "leading_size_constraints"),
      deleteIconBoxConstraints:
          parseBoxConstraints(widget.control, "delete_icon_size_constraints"),
      chipAnimationStyle: ChipAnimationStyle(
        enableAnimation:
            parseAnimationStyle(widget.control, "enable_animation_style"),
        selectAnimation:
            parseAnimationStyle(widget.control, "select_animation_style"),
        avatarDrawerAnimation: parseAnimationStyle(
            widget.control, "leading_drawer_animation_style"),
        deleteDrawerAnimation: parseAnimationStyle(
            widget.control, "delete_drawer_animation_style"),
      ),
      onPressed: onClick && !disabled
          ? () {
              backend.triggerControlEvent(widget.control, "click");
            }
          : null,
      onDeleted: onDelete && !disabled
          ? () {
              backend.triggerControlEvent(widget.control, "delete");
            }
          : null,
      onSelected: onSelect && !disabled
          ? (bool selected) {
              _selected = selected;
              backend.updateControl(widget.control.id, {"selected": selected});
              backend.triggerControlEvent(widget.control, "select", selected);
            }
          : null,
    );

    return ConstrainedControl(control: widget.control, child: chip);
  }
}
