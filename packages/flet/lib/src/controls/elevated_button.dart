import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import '../utils/others.dart';
import '../widgets/error.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';
import 'control_widget.dart';
import 'cupertino_button.dart';
import 'cupertino_dialog_action.dart';

class ElevatedButtonControl extends StatefulWidget {
  final Control control;

  const ElevatedButtonControl({
    super.key,
    required this.control,
  });

  @override
  State<ElevatedButtonControl> createState() => _ElevatedButtonControlState();
}

class _ElevatedButtonControlState extends State<ElevatedButtonControl>
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
    FletBackend.of(context).triggerControlEvent(
        widget.control, _focusNode.hasFocus ? "focus" : "blur");
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

      bool isFilledButton = widget.control.type == "FilledButton";
      bool isFilledTonalButton = widget.control.type == "FilledTonalButton";
      String text =
          widget.control.getString("text", "")!; // to be removed in 0.70.3
      String url = widget.control.getString("url", "")!;
      IconData? icon = parseIcon(widget.control.getString("icon"));
      Color? iconColor = widget.control.getColor("icon_color", context);
      var content = widget.control.get("content");
      Widget child = content is Control
          ? ControlWidget(control: content)
          : content is String
              ? Text(content)
              : Text(text); // to be changed to Text("") in 0.70.3

      var clipBehavior =
          parseClip(widget.control.getString("clip_behavior"), Clip.none)!;
      //bool onHover = widget.control.getBool("onHover", false)!;
      //bool onLongPress = widget.control.getBool("onLongPress", false)!;
      bool autofocus = widget.control.getBool("autofocus", false)!;

      Function()? onPressed = !widget.control.disabled
          ? () {
              debugPrint("Button ${widget.control.id} clicked!");
              if (url != "") {
                openWebBrowser(url,
                    webWindowName: widget.control.getString("url_target"));
              }
              FletBackend.of(context)
                  .triggerControlEvent(widget.control, "click");
            }
          : null;

      Function()? onLongPressHandler = !widget.control.disabled
          ? () {
              debugPrint("Button ${widget.control.id} long pressed!");
              FletBackend.of(context)
                  .triggerControlEvent(widget.control, "long_press");
            }
          : null;

      Function(bool)? onHoverHandler = !widget.control.disabled
          ? (state) {
              debugPrint("Button ${widget.control.id} hovered!");
              FletBackend.of(context).triggerControlEvent(
                  widget.control, "hover", state.toString());
            }
          : null;

      Widget? button;

      var theme = Theme.of(context);

      var style = parseButtonStyle(Theme.of(context), widget.control, "style",
          defaultForegroundColor: theme.colorScheme.primary,
          defaultBackgroundColor: theme.colorScheme.surface,
          defaultOverlayColor: theme.colorScheme.primary.withOpacity(0.08),
          defaultShadowColor: theme.colorScheme.shadow,
          defaultSurfaceTintColor: theme.colorScheme.surfaceTint,
          defaultElevation: 1,
          defaultPadding: const EdgeInsets.symmetric(horizontal: 8),
          defaultBorderSide: BorderSide.none,
          defaultShape: theme.useMaterial3
              ? const StadiumBorder()
              : RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)));

      if (icon != null) {
        if (child == const Text("")) {
          return const ErrorControl("Error displaying ElevatedButton",
              description:
                  "\"icon\" must be specified together with \"content\".");
        }
        if (isFilledButton) {
          button = FilledButton.icon(
              style: style,
              autofocus: autofocus,
              focusNode: _focusNode,
              onPressed: onPressed,
              onLongPress: onLongPressHandler,
              onHover: onHoverHandler,
              clipBehavior: clipBehavior,
              icon: Icon(
                icon,
                color: iconColor,
              ),
              label: child);
        } else if (isFilledTonalButton) {
          button = FilledButton.tonalIcon(
              style: style,
              autofocus: autofocus,
              focusNode: _focusNode,
              onPressed: onPressed,
              onLongPress: onLongPressHandler,
              onHover: onHoverHandler,
              clipBehavior: clipBehavior,
              icon: Icon(
                icon,
                color: iconColor,
              ),
              label: child);
        } else {
          button = ElevatedButton.icon(
              style: style,
              autofocus: autofocus,
              focusNode: _focusNode,
              onPressed: onPressed,
              onLongPress: onLongPressHandler,
              onHover: onHoverHandler,
              clipBehavior: clipBehavior,
              icon: Icon(
                icon,
                color: iconColor,
              ),
              label: child);
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
              child: child);
        } else if (isFilledTonalButton) {
          button = FilledButton.tonal(
              style: style,
              autofocus: autofocus,
              focusNode: _focusNode,
              onPressed: onPressed,
              onLongPress: onLongPressHandler,
              onHover: onHoverHandler,
              clipBehavior: clipBehavior,
              child: child);
        } else {
          button = ElevatedButton(
              style: style,
              autofocus: autofocus,
              focusNode: _focusNode,
              onPressed: onPressed,
              onLongPress: onLongPressHandler,
              onHover: onHoverHandler,
              clipBehavior: clipBehavior,
              child: child);
        }
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
