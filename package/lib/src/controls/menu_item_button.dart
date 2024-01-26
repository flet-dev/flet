import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/buttons.dart';
import 'create_control.dart';
import 'flet_control_stateful_mixin.dart';

class MenuItemButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const MenuItemButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  State<MenuItemButtonControl> createState() => _MenuItemButtonControlState();
}

class _MenuItemButtonControlState extends State<MenuItemButtonControl>
    with FletControlStatefulMixin {
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
    sendControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur", "");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("MenuItemButton build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var content =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    var leading =
        widget.children.where((c) => c.name == "leading" && c.isVisible);
    var trailing =
        widget.children.where((c) => c.name == "trailing" && c.isVisible);

    var clipBehavior = Clip.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            widget.control.attrString("clipBehavior", "")!.toLowerCase(),
        orElse: () => Clip.none);

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

    bool onClick = widget.control.attrBool("onClick", false)!;
    bool onHover = widget.control.attrBool("onHover", false)!;

    var menuItem = MenuItemButton(
      focusNode: _focusNode,
      clipBehavior: clipBehavior,
      style: style,
      closeOnActivate: widget.control.attrBool("closeOnClick", true)!,
      requestFocusOnHover: widget.control.attrBool("focusOnHover", true)!,
      onHover: onHover && !disabled
          ? (bool value) {
              sendControlEvent(widget.control.id, "hover", "$value");
            }
          : null,
      onPressed: onClick && !disabled
          ? () {
              sendControlEvent(widget.control.id, "click", "");
            }
          : null,
      leadingIcon: leading.isNotEmpty
          ? leading
              .map((c) => createControl(widget.control, c.id, disabled))
              .first
          : null,
      trailingIcon: trailing.isNotEmpty
          ? trailing
              .map((c) => createControl(widget.control, c.id, disabled))
              .first
          : null,
      child: content.isNotEmpty
          ? content
              .map((c) => createControl(widget.control, c.id, disabled))
              .first
          : null,
    );

    var focusValue = widget.control.attrString("focus");
    if (focusValue != null && focusValue != _lastFocusValue) {
      _lastFocusValue = focusValue;
      _focusNode.requestFocus();
    }

    return constrainedControl(context, menuItem, widget.parent, widget.control);
  }
}
