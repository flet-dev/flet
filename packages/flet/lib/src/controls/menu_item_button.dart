import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class MenuItemButtonControl extends StatefulWidget {
  final Control control;

  const MenuItemButtonControl({super.key, required this.control});

  @override
  State<MenuItemButtonControl> createState() => _MenuItemButtonControlState();
}

class _MenuItemButtonControlState extends State<MenuItemButtonControl> {
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
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("MenuItemButton build: ${widget.control.id}");

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

    bool onClick = widget.control.getBool("on_click", false)!;
    bool onHover = widget.control.getBool("on_hover", false)!;

    var menuItem = MenuItemButton(
      focusNode: _focusNode,
      clipBehavior: widget.control.getClipBehavior("clip_behavior", Clip.none)!,
      style: style,
      closeOnActivate: widget.control.getBool("close_on_click", true)!,
      requestFocusOnHover: widget.control.getBool("focus_on_hover", true)!,
      semanticsLabel: widget.control.getString("semantics_label"),
      autofocus: widget.control.getBool("autofocus", false)!,
      overflowAxis: widget.control.getAxis("overflow_axis", Axis.horizontal)!,
      onHover: onHover && !widget.control.disabled
          ? (bool value) => widget.control.triggerEvent("hover", data: value)
          : null,
      onPressed: onClick && !widget.control.disabled
          ? () => widget.control.triggerEvent("click")
          : null,
      leadingIcon: widget.control.buildWidget("leading"),
      trailingIcon: widget.control.buildWidget("trailing_icon"),
      child: widget.control.buildWidget("content"),
    );

    var focusValue = widget.control.getString("focus");
    if (focusValue != null && focusValue != _lastFocusValue) {
      _lastFocusValue = focusValue;
      _focusNode.requestFocus();
    }

    return ConstrainedControl(control: widget.control, child: menuItem);
  }
}
