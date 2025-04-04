import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../utils/launch_url.dart';
import '../widgets/error.dart';
import 'base_controls.dart';
import 'control_widget.dart';
import 'cupertino_button.dart';

class IconButtonControl extends StatefulWidget {
  final Control control;

  const IconButtonControl({
    super.key,
    required this.control,
  });

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
    widget.control.removeInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  void _onFocusChange() {
    FletBackend.of(context).triggerControlEvent(
        widget.control, _focusNode.hasFocus ? "focus" : "blur");
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
      Color? iconColor = widget.control.getColor("icon_color", context);
      Color? highlightColor =
          widget.control.getColor("highlight_color", context);
      Color? selectedIconColor =
          widget.control.getColor("selected_icon_color", context);
      Color? bgColor = widget.control.getColor("bgcolor", context);
      Color? disabledColor = widget.control.getColor("disabled_color", context);
      Color? hoverColor = widget.control.getColor("hover_color", context);
      Color? splashColor = widget.control.getColor("splash_color", context);
      Color? focusColor = widget.control.getColor("focus_color", context);
      double? iconSize = widget.control.getDouble("icon_size");
      double? splashRadius = widget.control.getDouble("splash_radius");
      var padding = parseEdgeInsets(widget.control, "padding");
      var alignment = parseAlignment(widget.control, "alignment");
      var sizeConstraints =
          parseBoxConstraints(widget.control, "size_constraints");
      bool autofocus = widget.control.getBool("autofocus", false)!;
      bool enableFeedback = widget.control.getBool("enable_feedback", true)!;
      bool selected = widget.control.getBool("selected", false)!;
      String url = widget.control.getString("url", "")!;
      String? urlTarget = widget.control.getString("urlTarget");
      var mouseCursor =
          parseMouseCursor(widget.control.getString("mouseCursor"));
      var visualDensity =
          parseVisualDensity(widget.control.getString("visualDensity"));

      Function()? onPressed = widget.control.disabled
          ? null
          : () {
              debugPrint("Button ${widget.control.id} clicked!");
              if (url != "") {
                openWebBrowser(url, webWindowName: urlTarget);
              }
              FletBackend.of(context)
                  .triggerControlEvent(widget.control, "click");
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

      Widget? iconWidget;
      if (icon is Control) {
        iconWidget = ControlWidget(control: icon);
      } else if (icon is String) {
        iconWidget = Icon(
          parseIcon(widget.control.getString("icon")),
          color: iconColor,
        );
      } else if (content != null) {
        iconWidget = ControlWidget(control: content);
      }

      Widget? selectedIconWidget;

      if (selectedIcon is Control) {
        selectedIconWidget = ControlWidget(control: selectedIcon);
      } else if (selectedIcon is String) {
        selectedIconWidget = Icon(
          parseIcon(widget.control.getString("selected_icon")),
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
            selectedIcon: selectedIconWidget,
            onPressed: onPressed);
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

      return ConstrainedControl(control: widget.control, child: button);
    });
  }
}
