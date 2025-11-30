import 'package:flutter/cupertino.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/geometry.dart';
import '../utils/launch_url.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class CupertinoButtonControl extends StatefulWidget {
  final Control control;

  CupertinoButtonControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<CupertinoButtonControl> createState() => _CupertinoButtonControlState();
}

class _CupertinoButtonControlState extends State<CupertinoButtonControl> {
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
    debugPrint("CupertinoButton.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown CupertinoButton method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoButton build: ${widget.control.id}");
    Color? iconColor = widget.control.getColor("icon_color", context);

    Widget? icon = widget.control.buildIconOrWidget("icon", color: iconColor);
    Widget? content = widget.control.buildTextOrWidget("content");

    Widget child;
    if (icon != null) {
      if (content != null) {
        child = Row(
            mainAxisSize: MainAxisSize.min,
            children: [icon, const SizedBox(width: 8), content]);
      } else {
        child = icon;
      }
    } else {
      child = content ?? const Text("");
    }

    var pressedOpacity = widget.control.getDouble("opacity_on_click", 0.4)!;
    var minSize = widget.control.getSize("min_size");
    var mouseCursor = widget.control.getMouseCursor("mouse_cursor");
    var autofocus = widget.control.getBool("autofocus", false)!;
    var bgColor = widget.control.getColor("bgcolor", context);
    var focusColor = widget.control.getColor("focus_color", context);
    var size = widget.control
        .getCupertinoButtonSize("size", CupertinoButtonSize.large)!;

    var alignment = widget.control.getAlignment("alignment", Alignment.center)!;
    var borderRadius = widget.control.getBorderRadius(
        "border_radius", const BorderRadius.all(Radius.circular(8.0)))!;

    var padding = widget.control.getPadding("padding");
    bool isFilledButton =
        {"CupertinoFilledButton", "FilledButton"}.contains(widget.control.type);
    bool isTintedButton = {"CupertinoTintedButton", "FilledTonalButton"}
        .contains(widget.control.type);

    // var style = widget.control.getButtonStyle("style", Theme.of(context),
    //     defaultForegroundColor: theme.colorScheme.primary,
    //     defaultBackgroundColor: Colors.transparent,
    //     defaultOverlayColor: Colors.transparent,
    //     defaultShadowColor: Colors.transparent,
    //     defaultSurfaceTintColor: Colors.transparent,
    //     defaultElevation: 0,
    //     defaultPadding: const EdgeInsets.all(8),
    //     defaultBorderSide: BorderSide.none,
    //     defaultShape: theme.useMaterial3
    //         ? const StadiumBorder()
    //         : RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)));

    // if (style != null) {
    //   Set<WidgetState> widgetStates = selected ? {WidgetState.selected} : {};

    //   // Check if the widget is disabled and update the foregroundColor accordingly
    //   // backgroundColor is not updated here, as it is handled by disabledColor
    //   if (control.disabled) {
    //     style = style.copyWith(
    //       foregroundColor: WidgetStatePropertyAll(theme.disabledColor),
    //     );
    //   }

    //   // Resolve color, background color, and padding based on widget states
    //   color = style.foregroundColor?.resolve(widgetStates);
    //   bgColor = style.backgroundColor?.resolve(widgetStates);
    //   padding = style.padding?.resolve({}) as EdgeInsets?;
    // }
    var color = widget.control.getColor("color", context);
    var disabledColor = widget.control.getColor(
        "disabled_bgcolor", context, CupertinoColors.tertiarySystemFill)!;
    if (color != null) {
      child = DefaultTextStyle(
          style: CupertinoTheme.of(context)
              .textTheme
              .textStyle
              .copyWith(color: color),
          child: child);
    }
    var url = widget.control.getUrl("url");
    Function()? onPressed = !widget.control.disabled
        ? () {
            if (url != null) {
              openWebBrowser(url);
            }
            widget.control.triggerEvent("click");
          }
        : null;
    Function()? onLongPressed = !widget.control.disabled
        ? () {
            widget.control.triggerEvent("long_press");
          }
        : null;

    CupertinoButton? button;
    if (isFilledButton) {
      button = CupertinoButton.filled(
        onPressed: onPressed,
        disabledColor: disabledColor,
        color: bgColor,
        padding: padding,
        borderRadius: borderRadius,
        pressedOpacity: pressedOpacity,
        alignment: alignment,
        minimumSize: minSize,
        sizeStyle: size,
        autofocus: autofocus,
        focusColor: focusColor,
        onLongPress: onLongPressed,
        focusNode: _focusNode,
        mouseCursor: mouseCursor,
        child: child,
      );
    } else if (isTintedButton) {
      button = CupertinoButton.tinted(
        onPressed: onPressed,
        disabledColor: disabledColor,
        color: bgColor,
        padding: padding,
        borderRadius: borderRadius,
        pressedOpacity: pressedOpacity,
        alignment: alignment,
        minimumSize: minSize,
        sizeStyle: size,
        autofocus: autofocus,
        focusColor: focusColor,
        onLongPress: onLongPressed,
        focusNode: _focusNode,
        mouseCursor: mouseCursor,
        child: child,
      );
    } else {
      button = CupertinoButton(
        onPressed: onPressed,
        disabledColor: disabledColor,
        color: bgColor,
        padding: padding,
        borderRadius: borderRadius,
        pressedOpacity: pressedOpacity,
        alignment: alignment,
        minimumSize: minSize,
        sizeStyle: size,
        autofocus: autofocus,
        focusColor: focusColor,
        onLongPress: onLongPressed,
        focusNode: _focusNode,
        mouseCursor: mouseCursor,
        child: child,
      );
    }

    return LayoutControl(control: widget.control, child: button);
  }
}
