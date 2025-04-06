import 'package:flutter/material.dart';

import '../controls/base_controls.dart';
import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import '../utils/misc.dart';
import '../widgets/flet_store_mixin.dart';
import 'control_widget.dart';
import 'cupertino_button.dart';
import 'cupertino_dialog_action.dart';

class TextButtonControl extends StatefulWidget {
  final Control control;

  const TextButtonControl({
    super.key,
    required this.control,
  });

  @override
  State<TextButtonControl> createState() => _TextButtonControlState();
}

class _TextButtonControlState extends State<TextButtonControl>
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
    widget.control.removeInvokeMethodListener(_invokeMethod);
    _focusNode.dispose();
    super.dispose();
  }

  void _onFocusChange() {
    FletBackend.of(context).triggerControlEvent(
        widget.control, _focusNode.hasFocus ? "focus" : "blur");
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("TextButton.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown TextButton method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Button build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      if (widget.control.adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return (widget.control.parent?.type == "AlertDialog" ||
                widget.control.parent?.type == "CupertinoAlertDialog")
            ? CupertinoDialogActionControl(
                control: widget.control,
              )
            : CupertinoButtonControl(
                control: widget.control,
              );
      }

      String text =
          widget.control.getString("text", "")!; //to be removed in 0.70.3
      var content = widget.control.get("content");
      var icon = widget.control.get("icon");
      var clipBehavior = parseClip(widget.control.getString("clip_behavior"));
      Color? iconColor = widget.control.getColor("icon_color", context);
      String url = widget.control.getString("url", "")!;
      String? urlTarget = widget.control.getString("url_target");
      bool autofocus = widget.control.getBool("autofocus", false)!;

      Widget contentWidget = content is Control
          ? ControlWidget(control: content)
          : content is String
              ? Text(content)
              : Text(text); // to be changed to Text("") in 0.70.3

      Widget? iconWidget;
      if (icon is Control) {
        iconWidget = ControlWidget(control: icon);
      } else if (icon is String) {
        iconWidget = Icon(
          parseIcon(widget.control.getString("icon")),
          color: iconColor,
        );
      }

      Function()? onPressed = widget.control.disabled
          ? null
          : () {
              if (url != "") {
                openWebBrowser(url, webWindowName: urlTarget);
              }
              FletBackend.of(context)
                  .triggerControlEvent(widget.control, "click");
            };

      Function()? onLongPressHandler = widget.control.disabled
          ? null
          : () {
              FletBackend.of(context)
                  .triggerControlEvent(widget.control, "long_press");
            };

      Function(bool)? onHoverHandler = widget.control.disabled
          ? null
          : (state) {
              FletBackend.of(context).triggerControlEvent(
                  widget.control, "hover", state.toString());
            };

      TextButton? button;

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

      if (icon != null) {
        button = TextButton.icon(
            autofocus: autofocus,
            focusNode: _focusNode,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            style: style,
            clipBehavior: clipBehavior,
            icon: iconWidget,
            label: contentWidget);
      } else {
        button = TextButton(
            autofocus: autofocus,
            focusNode: _focusNode,
            style: style,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            clipBehavior: clipBehavior,
            child: contentWidget);
      }

      return ConstrainedControl(control: widget.control, child: button);
    });
  }
}
