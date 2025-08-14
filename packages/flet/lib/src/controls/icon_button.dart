import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'control_widget.dart';
import 'cupertino_button.dart';

class IconButtonControl extends StatefulWidget {
  final Control control;

  IconButtonControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<IconButtonControl> createState() => _IconButtonControlState();
}

class _IconButtonControlState extends State<IconButtonControl>
    with FletStoreMixin {
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  void _onFocusChange() {
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("IconButton.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown IconButton method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("IconButton build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      if (widget.control.adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoButtonControl(
          control: widget.control,
        );
      }

      var icon = widget.control.get("icon");
      var selectedIcon = widget.control.get("selected_icon");
      var content = widget.control.child("content");
      var iconColor = widget.control.getColor("icon_color", context);
      var highlightColor = widget.control.getColor("highlight_color", context);
      var selectedIconColor =
          widget.control.getColor("selected_icon_color", context);
      var bgcolor = widget.control.getColor("bgcolor", context);
      var disabledColor = widget.control.getColor("disabled_color", context);
      var hoverColor = widget.control.getColor("hover_color", context);
      var splashColor = widget.control.getColor("splash_color", context);
      var focusColor = widget.control.getColor("focus_color", context);
      var iconSize = widget.control.getDouble("icon_size");
      var splashRadius = widget.control.getDouble("splash_radius");
      var padding = widget.control.getEdgeInsets("padding");
      var alignment = widget.control.getAlignment("alignment");
      var sizeConstraints =
          widget.control.getBoxConstraints("size_constraints");
      var autofocus = widget.control.getBool("autofocus", false)!;
      var enableFeedback = widget.control.getBool("enable_feedback", true)!;
      var selected = widget.control.getBool("selected", false)!;
      var url = widget.control.getString("url");
      var urlTarget = widget.control.getString("url_target");
      var mouseCursor = widget.control.getMouseCursor("mouse_cursor");
      var visualDensity = widget.control.getVisualDensity("visual_density");

      Function()? onPressed = !widget.control.disabled
          ? () {
              if (url != null) {
                openWebBrowser(url, webWindowName: urlTarget);
              }
              widget.control.triggerEvent("click");
            }
          : null;

      Function()? onLongPressHandler = !widget.control.disabled
          ? () => widget.control.triggerEvent("long_press")
          : null;

      Function(bool)? onHoverHandler = !widget.control.disabled
          ? (bool hovered) => FletBackend.of(context)
              .triggerControlEvent(widget.control, "hover", hovered)
          : null;

      Widget? button;

      var theme = Theme.of(context);
      var style = parseButtonStyle(
          widget.control.get("style"), Theme.of(context),
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

      Widget? iconWidget;
      if (icon is Control) {
        iconWidget = ControlWidget(control: icon);
      } else if (icon is int) {
        iconWidget = Icon(
          widget.control.getIconData("icon"),
          color: iconColor,
        );
      } else if (content != null) {
        iconWidget = ControlWidget(control: content);
      }

      Widget? selectedIconWidget;

      if (selectedIcon is Control) {
        selectedIconWidget = ControlWidget(control: selectedIcon);
      } else if (selectedIcon is int) {
        selectedIconWidget = Icon(
          widget.control.getIconData("selected_icon"),
          color: selectedIconColor,
        );
      }

      if (iconWidget != null) {
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
            icon: iconWidget,
            iconSize: iconSize,
            mouseCursor: mouseCursor,
            visualDensity: visualDensity,
            style: style,
            isSelected: selected,
            constraints: sizeConstraints,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            selectedIcon: selectedIconWidget,
            onPressed: onPressed);
      } else {
        return const ErrorControl(
            "IconButton must have either icon or a visible content specified.");
      }

      if (bgcolor != null) {
        button = Container(
          decoration:
              ShapeDecoration(color: bgcolor, shape: const CircleBorder()),
          child: button,
        );
      }

      return ConstrainedControl(control: widget.control, child: button);
    });
  }
}
