import 'package:flet/src/controls/cupertino_button.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_control_stateful_mixin.dart';
import 'flet_store_mixin.dart';

class ElevatedButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const ElevatedButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  State<ElevatedButtonControl> createState() => _ElevatedButtonControlState();
}

class _ElevatedButtonControlState extends State<ElevatedButtonControl>
    with FletControlStatefulMixin, FletStoreMixin {
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
    debugPrint("Button build: ${widget.control.id}");

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
            children: widget.children);
      }

      String text = widget.control.attrString("text", "")!;
      String url = widget.control.attrString("url", "")!;
      IconData? icon = parseIcon(widget.control.attrString("icon", "")!);
      Color? iconColor = HexColor.fromString(
          Theme.of(context), widget.control.attrString("iconColor", "")!);
      var contentCtrls = widget.children.where((c) => c.name == "content");
      bool onHover = widget.control.attrBool("onHover", false)!;
      bool onLongPress = widget.control.attrBool("onLongPress", false)!;
      bool autofocus = widget.control.attrBool("autofocus", false)!;
      bool disabled = widget.control.isDisabled || widget.parentDisabled;

      Function()? onPressed = !disabled
          ? () {
              debugPrint("Button ${widget.control.id} clicked!");
              if (url != "") {
                openWebBrowser(url,
                    webWindowName: widget.control.attrString("urlTarget"));
              }
              sendControlEvent(widget.control.id, "click", "");
            }
          : null;

      Function()? onLongPressHandler = onLongPress && !disabled
          ? () {
              debugPrint("Button ${widget.control.id} long pressed!");
              sendControlEvent(widget.control.id, "long_press", "");
            }
          : null;

      Function(bool)? onHoverHandler = onHover && !disabled
          ? (state) {
              debugPrint("Button ${widget.control.id} hovered!");
              sendControlEvent(widget.control.id, "hover", state.toString());
            }
          : null;

      ElevatedButton? button;

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
        if (text == "") {
          return const ErrorControl("Error displaying ElevatedButton",
              description:
                  "\"icon\" must be specified together with \"text\".");
        }
        button = ElevatedButton.icon(
            style: style,
            autofocus: autofocus,
            focusNode: _focusNode,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            icon: Icon(
              icon,
              color: iconColor,
            ),
            label: Text(text));
      } else if (contentCtrls.isNotEmpty) {
        button = ElevatedButton(
            style: style,
            autofocus: autofocus,
            focusNode: _focusNode,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            child: createControl(
                widget.control, contentCtrls.first.id, disabled,
                parentAdaptive: adaptive));
      } else {
        button = ElevatedButton(
            style: style,
            autofocus: autofocus,
            focusNode: _focusNode,
            onPressed: onPressed,
            onLongPress: onLongPressHandler,
            onHover: onHoverHandler,
            child: Text(text));
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
