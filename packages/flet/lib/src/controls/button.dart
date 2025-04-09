import 'package:flet/flet.dart';
import 'package:flet/src/widgets/error.dart';
import 'package:flutter/material.dart';

import 'base_controls.dart';

class ButtonControl extends StatefulWidget {
  final Control control;

  const ButtonControl({
    super.key,
    required this.control,
  });

  @override
  State<ButtonControl> createState() => _ButtonControlState();
}

class _ButtonControlState extends State<ButtonControl> with FletStoreMixin {
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
    debugPrint("Button.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown Button method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Button build: ${widget.control.id}");

    bool isFilledButton = widget.control.type == "FilledButton";
    bool isFilledTonalButton = widget.control.type == "FilledTonalButton";
    bool isTextButton = widget.control.type == "TextButton";
    bool isOutlinedButton = widget.control.type == "OutlinedButton";
    String url = widget.control.getString("url", "")!;
    Color? iconColor = widget.control.getColor("icon_color", context);

    Widget? iconWidget =
        widget.control.buildIconOrWidget("icon", color: iconColor);

    var clipBehavior =
        widget.control.getClipBehavior("clip_behavior", Clip.none)!;
    bool autofocus = widget.control.getBool("autofocus", false)!;

    Function()? onPressed = !widget.control.disabled
        ? () {
            if (url != "") {
              openWebBrowser(url,
                  webWindowName: widget.control.getString("url_target"));
            }
            widget.control.triggerEvent("click");
          }
        : null;

    Function()? onLongPressHandler = !widget.control.disabled
        ? () {
            widget.control.triggerEvent("long_press");
          }
        : null;

    Function(bool)? onHoverHandler = !widget.control.disabled
        ? (state) {
            widget.control.triggerEvent("hover", state);
          }
        : null;

    Widget? button;

    var theme = Theme.of(context);

    var style = widget.control.getButtonStyle("style", Theme.of(context),
        defaultForegroundColor: widget.control
            .getColor("color", context, theme.colorScheme.primary)!,
        defaultBackgroundColor: widget.control
            .getColor("bgcolor", context, theme.colorScheme.surface)!,
        defaultOverlayColor: theme.colorScheme.primary.withOpacity(0.08),
        defaultShadowColor: theme.colorScheme.shadow,
        defaultSurfaceTintColor: theme.colorScheme.surfaceTint,
        defaultElevation: widget.control.getDouble("elevation", 1)!,
        defaultPadding: const EdgeInsets.symmetric(horizontal: 8),
        defaultBorderSide: BorderSide.none,
        defaultShape: theme.useMaterial3
            ? const StadiumBorder()
            : RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)));

    Widget error = const ErrorControl("Error displaying Button",
        description: "\"icon\" must be specified together with \"content\"");

    if (iconWidget != null) {
      if (isFilledButton) {
        button = FilledButton.icon(
            style: style,
            autofocus: autofocus,
            focusNode: _focusNode,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            clipBehavior: clipBehavior,
            icon: iconWidget,
            label: widget.control.buildTextOrWidget("content",
                textPropertyName: "text", required: true, error: error)!);
      } else if (isFilledTonalButton) {
        button = FilledButton.tonalIcon(
            style: style,
            autofocus: autofocus,
            focusNode: _focusNode,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            clipBehavior: clipBehavior,
            icon: iconWidget,
            label: widget.control.buildTextOrWidget("content",
                textPropertyName: "text", required: true, error: error)!);
      } else if (isTextButton) {
        button = TextButton.icon(
          autofocus: autofocus,
          focusNode: _focusNode,
          onPressed: onPressed,
          onLongPress: onLongPressHandler,
          onHover: onHoverHandler,
          style: style,
          clipBehavior: clipBehavior,
          icon: widget.control.buildIconOrWidget("icon", color: iconColor),
          label: widget.control
                  .buildTextOrWidget("content", textPropertyName: "text") ??
              const Text(""),
        );
      } else {
        button = ElevatedButton.icon(
            style: style,
            autofocus: autofocus,
            focusNode: _focusNode,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            clipBehavior: clipBehavior,
            icon: iconWidget,
            label: widget.control.buildTextOrWidget("content",
                textPropertyName: "text", required: true, error: error)!);
      }
    } else {
      if (isFilledButton) {
        button = FilledButton(
            style: style,
            autofocus: autofocus,
            focusNode: _focusNode,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            clipBehavior: clipBehavior,
            child: widget.control
                .buildTextOrWidget("content", textPropertyName: "text"));
      } else if (isFilledTonalButton) {
        button = FilledButton.tonal(
            style: style,
            autofocus: autofocus,
            focusNode: _focusNode,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            clipBehavior: clipBehavior,
            child: widget.control
                .buildTextOrWidget("content", textPropertyName: "text"));
      } else if (isTextButton) {
        button = TextButton(
            autofocus: autofocus,
            focusNode: _focusNode,
            style: style,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            clipBehavior: clipBehavior,
            child: widget.control
                    .buildTextOrWidget("content", textPropertyName: "text") ??
                const Text(""));
      } else {
        button = ElevatedButton(
            style: style,
            autofocus: autofocus,
            focusNode: _focusNode,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            clipBehavior: clipBehavior,
            child: widget.control
                .buildTextOrWidget("content", textPropertyName: "text"));
      }
    }

    return ConstrainedControl(control: widget.control, child: button);
  }
}
