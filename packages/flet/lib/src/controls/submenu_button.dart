import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/menu.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/transforms.dart';
import 'base_controls.dart';

class SubmenuButtonControl extends StatefulWidget {
  final Control control;

  const SubmenuButtonControl({super.key, required this.control});

  @override
  State<SubmenuButtonControl> createState() => _SubmenuButtonControlState();
}

class _SubmenuButtonControlState extends State<SubmenuButtonControl> {
  late final FocusNode _focusNode;
  String? _lastFocusValue;

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

  void _onFocusChange() {
    widget.control
        .triggerEvent(_focusNode.hasFocus ? "focus" : "blur", context);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SubMenuButton build: ${widget.control.id}");

    var theme = Theme.of(context);
    var style = widget.control.getButtonStyle("style", Theme.of(context),
        defaultForegroundColor: theme.colorScheme.primary,
        defaultBackgroundColor: Colors.transparent,
        defaultOverlayColor: Colors.transparent,
        defaultShadowColor: Colors.transparent,
        defaultSurfaceTintColor: Colors.transparent,
        defaultElevation: 0,
        defaultPadding: const EdgeInsets.all(8),
        defaultBorderSide: BorderSide.none,
        defaultShape: theme.useMaterial3
            ? const StadiumBorder()
            : RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)));

    bool onOpen = widget.control.getBool("on_open", false)!;
    bool onClose = widget.control.getBool("on_close", false)!;
    bool onHover = widget.control.getBool("on_hover", false)!;

    var subMenuButton = SubmenuButton(
      focusNode: _focusNode,
      clipBehavior:
          widget.control.getClipBehavior("clip_behavior", Clip.hardEdge)!,
      style: style,
      menuStyle: widget.control.getMenuStyle("menu_style", Theme.of(context)),
      alignmentOffset: widget.control.getOffset("alignment_offset"),
      onClose: onClose && !widget.control.disabled
          ? () => widget.control.triggerEvent("close", context)
          : null,
      onHover: onHover && !widget.control.disabled
          ? (bool value) => widget.control.triggerEvent("hover", context, value)
          : null,
      onOpen: onOpen && !widget.control.disabled
          ? () => widget.control.triggerEvent("open", context)
          : null,
      leadingIcon: widget.control.buildWidget("leading"),
      trailingIcon: widget.control.buildWidget("trailing"),
      menuChildren: widget.control.buildWidgets("controls"),
      child: widget.control.buildWidget("content"),
    );

    var focusValue = widget.control.getString("focus");
    if (focusValue != null && focusValue != _lastFocusValue) {
      _lastFocusValue = focusValue;
      _focusNode.requestFocus();
    }

    return ConstrainedControl(control: widget.control, child: subMenuButton);
  }
}
