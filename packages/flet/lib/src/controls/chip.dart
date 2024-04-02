import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
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
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var labelCtrls =
        widget.children.where((c) => c.name == "label" && c.isVisible);
    var leadingCtrls =
        widget.children.where((c) => c.name == "leading" && c.isVisible);
    var deleteIconCtrls =
        widget.children.where((c) => c.name == "deleteIcon" && c.isVisible);

    if (labelCtrls.isEmpty) {
      return const ErrorControl("Chip must have label specified.");
    }

    double? clickElevation = widget.control.attrDouble("clickElevation");
    Color? bgcolor = widget.control.attrColor("bgcolor", context);
    Color? deleteIconColor =
        widget.control.attrColor("deleteIconColor", context);
    Color? disabledColor = widget.control.attrColor("disabledColor", context);
    Color? surfaceTintColor =
        widget.control.attrColor("surfaceTintColor", context);
    Color? selectedShadowColor =
        widget.control.attrColor("selectedShadowColor", context);
    Color? shadowColor = widget.control.attrColor("shadowColor", context);
    var color =
        parseMaterialStateColor(Theme.of(context), widget.control, "color");

    BorderSide? borderSide =
        parseBorderSide(Theme.of(context), widget.control, "borderSide");
    VisualDensity? visualDensity =
        parseVisualDensity(widget.control.attrString("visualDensity"), null);
    Clip clipBehavior = Clip.values.firstWhere(
        (c) => c.toString() == widget.control.attrString("clipBehavior", "")!,
        orElse: () => Clip.none);

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
            widget.backend.triggerControlEvent(widget.control.id, "click");
          }
        : null;

    Function()? onDeleteHandler = onDelete && !disabled
        ? () {
            debugPrint("Chip ${widget.control.id} deleted!");
            widget.backend.triggerControlEvent(widget.control.id, "delete");
          }
        : null;

    return constrainedControl(
        context,
        InputChip(
          autofocus: autofocus,
          focusNode: _focusNode,
          label: createControl(widget.control, labelCtrls.first.id, disabled,
              parentAdaptive: widget.parentAdaptive),
          avatar: leadingCtrls.isNotEmpty
              ? createControl(widget.control, leadingCtrls.first.id, disabled,
                  parentAdaptive: widget.parentAdaptive)
              : null,
          backgroundColor: bgcolor,
          checkmarkColor: widget.control.attrColor("checkColor", context),
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
                  widget.control, deleteIconCtrls.first.id, disabled,
                  parentAdaptive: widget.parentAdaptive)
              : null,
          deleteIconColor: deleteIconColor,
          disabledColor: disabledColor,
          elevation: elevation,
          isEnabled: !disabled,
          padding: parseEdgeInsets(widget.control, "padding"),
          labelPadding: parseEdgeInsets(widget.control, "labelPadding"),
          labelStyle:
              parseTextStyle(Theme.of(context), widget.control, "labelStyle"),
          selectedColor: widget.control.attrColor("selectedColor", context),
          selectedShadowColor: selectedShadowColor,
          shadowColor: shadowColor,
          shape: parseOutlinedBorder(widget.control, "shape"),
          color: color,
          surfaceTintColor: surfaceTintColor,
          pressElevation: clickElevation,
          side: borderSide,
          clipBehavior: clipBehavior,
          visualDensity: visualDensity,
        ),
        widget.parent,
        widget.control);
  }
}
