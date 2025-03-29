import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/others.dart';
import 'create_control.dart';

class MenuItemButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const MenuItemButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

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
    widget.backend.triggerControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("MenuItemButton build: ${widget.control.id}");
    bool disabled = widget.control.disabled || widget.parentDisabled;

    var content =
        widget.children.where((c) => c.name == "content" && c.visible);
    var leading =
        widget.children.where((c) => c.name == "leading" && c.visible);
    var trailing =
        widget.children.where((c) => c.name == "trailing" && c.visible);

    var theme = Theme.of(context);
    var style = parseButtonStyle(Theme.of(context), widget.control, "style",
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

    bool onClick = widget.control.getBool("onClick", false)!;
    bool onHover = widget.control.getBool("onHover", false)!;

    var adaptive = widget.control.adaptive ?? widget.parentAdaptive;

    var menuItem = MenuItemButton(
      focusNode: _focusNode,
      clipBehavior:
          parseClip(widget.control.getString("clipBehavior"), Clip.none)!,
      style: style,
      closeOnActivate: widget.control.getBool("closeOnClick", true)!,
      requestFocusOnHover: widget.control.getBool("focusOnHover", true)!,
      semanticsLabel: widget.control.getString("semanticsLabel"),
      autofocus: widget.control.getBool("autofocus", false)!,
      overflowAxis:
          parseAxis(widget.control.getString("overflowAxis"), Axis.horizontal)!,
      onHover: onHover && !disabled
          ? (bool value) {
              widget.backend
                  .triggerControlEvent(widget.control.id, "hover", "$value");
            }
          : null,
      onPressed: onClick && !disabled
          ? () {
              widget.backend.triggerControlEvent(widget.control.id, "click");
            }
          : null,
      leadingIcon: leading.isNotEmpty
          ? createControl(widget.control, leading.first.id, disabled,
              parentAdaptive: adaptive)
          : null,
      trailingIcon: trailing.isNotEmpty
          ? createControl(widget.control, trailing.first.id, disabled,
              parentAdaptive: adaptive)
          : null,
      child: content.isNotEmpty
          ? createControl(widget.control, content.first.id, disabled,
              parentAdaptive: adaptive)
          : null,
    );

    var focusValue = widget.control.getString("focus");
    if (focusValue != null && focusValue != _lastFocusValue) {
      _lastFocusValue = focusValue;
      _focusNode.requestFocus();
    }

    return constrainedControl(context, menuItem, widget.parent, widget.control);
  }
}
