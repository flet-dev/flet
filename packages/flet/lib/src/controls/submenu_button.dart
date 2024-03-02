import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/menu.dart';
import '../utils/transforms.dart';
import 'create_control.dart';

class SubMenuButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const SubMenuButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  State<SubMenuButtonControl> createState() => _SubMenuButtonControlState();
}

class _SubMenuButtonControlState extends State<SubMenuButtonControl> {
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
    debugPrint("SubMenuButton build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var content =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    var ctrls =
        widget.children.where((c) => c.name == "controls" && c.isVisible);
    var leading =
        widget.children.where((c) => c.name == "leading" && c.isVisible);
    var trailing =
        widget.children.where((c) => c.name == "trailing" && c.isVisible);

    var clipBehavior = Clip.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            widget.control.attrString("clipBehavior", "")!.toLowerCase(),
        orElse: () => Clip.hardEdge);

    var offsetDetails = parseOffset(widget.control, "alignmentOffset");

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

    var menuStyle =
        parseMenuStyle(Theme.of(context), widget.control, "menuStyle");

    bool onOpen = widget.control.attrBool("onOpen", false)!;
    bool onClose = widget.control.attrBool("onClose", false)!;
    bool onHover = widget.control.attrBool("onHover", false)!;

    var subMenu = SubmenuButton(
      focusNode: _focusNode,
      clipBehavior: clipBehavior,
      style: style,
      menuStyle: menuStyle,
      alignmentOffset: offsetDetails != null
          ? Offset(offsetDetails.x, offsetDetails.y)
          : null,
      onClose: onClose && !disabled
          ? () {
              widget.backend.triggerControlEvent(widget.control.id, "close");
            }
          : null,
      onHover: onHover && !disabled
          ? (bool value) {
              widget.backend
                  .triggerControlEvent(widget.control.id, "hover", "$value");
            }
          : null,
      onOpen: onOpen && !disabled
          ? () {
              widget.backend.triggerControlEvent(widget.control.id, "open");
            }
          : null,
      leadingIcon: leading.isNotEmpty
          ? leading
              .map((c) => createControl(widget.control, c.id, disabled))
              .toList()
              .first
          : null,
      trailingIcon: trailing.isNotEmpty
          ? trailing
              .map((c) => createControl(widget.control, c.id, disabled))
              .toList()
              .first
          : null,
      menuChildren: ctrls.isNotEmpty
          ? ctrls.map((c) {
              return createControl(widget.control, c.id, disabled);
            }).toList()
          : [],
      child: content.isNotEmpty
          ? content
              .map((c) => createControl(widget.control, c.id, disabled))
              .toList()
              .first
          : null,
    );

    var focusValue = widget.control.attrString("focus");
    if (focusValue != null && focusValue != _lastFocusValue) {
      _lastFocusValue = focusValue;
      _focusNode.requestFocus();
    }

    return constrainedControl(context, subMenu, widget.parent, widget.control);
  }
}
