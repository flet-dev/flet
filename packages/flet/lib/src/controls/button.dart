import 'package:flet/flet.dart';
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
    // String text =
    //     widget.control.getString("text", "")!; //(todo 0.70.3) remove text
    String url = widget.control.getString("url", "")!;
    Color? iconColor = widget.control.getColor("icon_color", context);

    Widget? iconWidget =
        widget.control.buildIconOrWidget("icon", color: iconColor);

    //var content = widget.control.get("content");
    // Widget contentWidget = content is Control
    //     ? ControlWidget(control: content)
    //     : content is String
    //         ? Text(content)
    //         : Text(text); //(todo 0.70.3) change to Text("")

    //Widget? contentWidget = widget.control.buildTextOrWidget("content")!;

    var clipBehavior =
        parseClip(widget.control.getString("clip_behavior"), Clip.none)!;
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

    if (iconWidget != null) {
      // if (contentWidget == const Text("")) {
      //   return const ErrorControl("Error displaying ElevatedButton",
      //       description:
      //           "\"icon\" must be specified together with \"content\"");
      // }
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
            //label: contentWidget
            label: widget.control.buildTextOrWidget("content",
                textPropertyName: "text", required: true)!);
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
                textPropertyName: "text", required: true)!);
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
                textPropertyName: "text", required: true)!);
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
    // });
  }
}
