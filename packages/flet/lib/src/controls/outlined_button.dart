import 'package:flet/src/extensions/control.dart';
import 'package:flet/src/utils/colors.dart';
import 'package:flet/src/utils/misc.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';
import 'cupertino_button.dart';
import 'cupertino_dialog_action.dart';

class OutlinedButtonControl extends StatefulWidget {
  final Control control;

  const OutlinedButtonControl({super.key, required this.control});

  @override
  State<OutlinedButtonControl> createState() => _OutlinedButtonControlState();
}

class _OutlinedButtonControlState extends State<OutlinedButtonControl>
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
    widget.control
        .triggerEvent(_focusNode.hasFocus ? "focus" : "blur", context);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Button build: ${widget.control.id}");

    var text = widget.control.getString("text", "")!;
    var icon = parseIcon(widget.control.getString("icon"));
    var iconColor = widget.control.getColor("icon_color", context);
    var content = widget.control.buildWidget("content") ?? Text(text);
    var url = widget.control.getString("url", "")!;
    var urlTarget = widget.control.getString("url_target");
    var onHover = widget.control.getBool("on_hover", false)!;
    var onLongPress = widget.control.getBool("on_long_press", false)!;
    var autofocus = widget.control.getBool("autofocus", false)!;
    var clipBehavior =
        widget.control.getClipBehavior("clip_behavior", Clip.none)!;
    Function()? onPressed = !widget.control.disabled
        ? () {
            if (url != "") {
              openWebBrowser(url, webWindowName: urlTarget);
            }
            widget.control.triggerEvent("click", context);
          }
        : null;

    Function()? onLongPressHandler = onLongPress && !widget.control.disabled
        ? () => widget.control.triggerEvent("long_press", context)
        : null;

    Function(bool)? onHoverHandler = onHover && !widget.control.disabled
        ? (state) => widget.control.triggerEvent("hover", context, state)
        : null;

    return withPagePlatform((context, platform) {
      if (widget.control.adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        var actions = widget.control.buildWidgets("actions");
        return actions.isNotEmpty &&
                ["AlertDialog", "CupertinoAlertDialog"]
                    .contains(widget.control.parent?.type)
            ? CupertinoDialogActionControl(control: widget.control)
            : CupertinoButtonControl(control: widget.control);
      }

      var theme = Theme.of(context);
      var style = widget.control.getButtonStyle("style", theme,
          defaultForegroundColor: theme.colorScheme.primary,
          defaultBackgroundColor: Colors.transparent,
          defaultOverlayColor: Colors.transparent,
          defaultShadowColor: Colors.transparent,
          defaultSurfaceTintColor: Colors.transparent,
          defaultElevation: 0,
          defaultPadding: const EdgeInsets.all(8),
          defaultBorderSide: BorderSide(color: theme.colorScheme.outline),
          defaultShape: theme.useMaterial3
              ? const StadiumBorder()
              : RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)));

      OutlinedButton? button;
      if (icon != null) {
        button = OutlinedButton.icon(
            autofocus: autofocus,
            focusNode: _focusNode,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            clipBehavior: clipBehavior,
            style: style,
            icon: Icon(icon, color: iconColor),
            label: Text(text));
      } else {
        button = OutlinedButton(
            autofocus: autofocus,
            focusNode: _focusNode,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            clipBehavior: clipBehavior,
            onHover: onHoverHandler,
            style: style,
            child: content);
      }

      var focusValue = widget.control.getString("focus");
      if (focusValue != null && focusValue != _lastFocusValue) {
        _lastFocusValue = focusValue;
        _focusNode.requestFocus();
      }

      return ConstrainedControl(control: widget.control, child: button);
    });
  }
}
