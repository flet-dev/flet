import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/box.dart';
import '../utils/buttons.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import '../utils/mouse.dart';
import '../utils/theme.dart';
import 'create_control.dart';
import 'cupertino_button.dart';
import 'error.dart';
import 'flet_store_mixin.dart';

class IconButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const IconButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<IconButtonControl> createState() => _IconButtonControlState();
}

class _IconButtonControlState extends State<IconButtonControl>
    with FletStoreMixin {
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
    debugPrint("IconButton build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      bool? adaptive =
          widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
      if (adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoButtonControl(
            control: widget.control,
            parentDisabled: widget.parentDisabled,
            parentAdaptive: adaptive,
            children: widget.children,
            backend: widget.backend);
      }

      IconData? icon = parseIcon(widget.control.attrString("icon"));
      IconData? selectedIcon =
          parseIcon(widget.control.attrString("selectedIcon"));
      Color? iconColor = widget.control.attrColor("iconColor", context);
      Color? highlightColor =
          widget.control.attrColor("highlightColor", context);
      Color? selectedIconColor =
          widget.control.attrColor("selectedIconColor", context);
      Color? bgColor = widget.control.attrColor("bgColor", context);
      Color? disabledColor = widget.control.attrColor("disabledColor", context);
      Color? hoverColor = widget.control.attrColor("hoverColor", context);
      Color? splashColor = widget.control.attrColor("splashColor", context);
      Color? focusColor = widget.control.attrColor("focusColor", context);
      double? iconSize = widget.control.attrDouble("iconSize");
      double? splashRadius = widget.control.attrDouble("splashRadius");
      var padding = parseEdgeInsets(widget.control, "padding");
      var alignment = parseAlignment(widget.control, "alignment");
      var sizeConstraints =
          parseBoxConstraints(widget.control, "sizeConstraints");
      var contentCtrls =
          widget.children.where((c) => c.name == "content" && c.isVisible);
      bool autofocus = widget.control.attrBool("autofocus", false)!;
      bool enableFeedback = widget.control.attrBool("enableFeedback", true)!;
      bool selected = widget.control.attrBool("selected", false)!;
      String url = widget.control.attrString("url", "")!;
      String? urlTarget = widget.control.attrString("urlTarget");
      bool disabled = widget.control.isDisabled || widget.parentDisabled;
      var mouseCursor =
          parseMouseCursor(widget.control.attrString("mouseCursor"));
      var visualDensity =
          parseVisualDensity(widget.control.attrString("visualDensity"));

      Function()? onPressed = disabled
          ? null
          : () {
              debugPrint("Button ${widget.control.id} clicked!");
              if (url != "") {
                openWebBrowser(url, webWindowName: urlTarget);
              }
              widget.backend.triggerControlEvent(widget.control.id, "click");
            };

      Widget? button;

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

      if (icon != null) {
        button = IconButton(
            autofocus: autofocus,
            focusNode: _focusNode,
            highlightColor: highlightColor,
            disabledColor: disabledColor,
            hoverColor: hoverColor,
            enableFeedback: enableFeedback,
            padding: padding,
            alignment: alignment,
            focusColor: focusColor,
            splashColor: splashColor,
            splashRadius: splashRadius,
            icon: Icon(
              icon,
              color: iconColor,
            ),
            iconSize: iconSize,
            mouseCursor: mouseCursor,
            visualDensity: visualDensity,
            style: style,
            isSelected: selected,
            constraints: sizeConstraints,
            selectedIcon: selectedIcon != null
                ? Icon(selectedIcon, color: selectedIconColor)
                : null,
            onPressed: onPressed);
      } else if (contentCtrls.isNotEmpty) {
        button = IconButton(
            autofocus: autofocus,
            focusNode: _focusNode,
            highlightColor: highlightColor,
            disabledColor: highlightColor,
            hoverColor: highlightColor,
            enableFeedback: enableFeedback,
            padding: padding,
            alignment: alignment,
            focusColor: focusColor,
            splashColor: splashColor,
            splashRadius: splashRadius,
            onPressed: onPressed,
            iconSize: iconSize,
            mouseCursor: mouseCursor,
            visualDensity: visualDensity,
            style: style,
            isSelected: selected,
            constraints: sizeConstraints,
            selectedIcon: selectedIcon != null
                ? Icon(selectedIcon, color: selectedIconColor)
                : null,
            icon: createControl(widget.control, contentCtrls.first.id, disabled,
                parentAdaptive: widget.parentAdaptive));
      } else {
        return const ErrorControl(
            "IconButton must have either icon or a visible content specified.");
      }

      if (bgColor != null) {
        button = Container(
          decoration:
              ShapeDecoration(color: bgColor, shape: const CircleBorder()),
          child: button,
        );
      }

      var focusValue = widget.control.attrString("focus");
      if (focusValue != null && focusValue != _lastFocusValue) {
        _lastFocusValue = focusValue;
        _focusNode.requestFocus();
      }

      return constrainedControl(context, button, widget.parent, widget.control);
    });
  }
}
