import 'package:flet/src/utils/alignment.dart';
import 'package:flet/src/utils/borders.dart';
import 'package:flet/src/utils/edge_insets.dart';
import 'package:flet/src/utils/icons.dart';
import 'package:flutter/cupertino.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/launch_url.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';
import 'control_widget.dart';

class CupertinoButtonControl extends StatefulWidget {
  final Control control;

  const CupertinoButtonControl({
    super.key,
    required this.control,
  });

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
    debugPrint("ElevatedButton.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown ElevatedButton method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoButton build: ${widget.control.id}");
    // var theme = Theme.of(context);
    String text =
        widget.control.getString("text", "")!; //(todo 0.70.3) remove text
    var content = widget.control.get("content");
    Widget contentWidget = content is Control
        ? ControlWidget(control: content)
        : content is String
            ? Text(content)
            : Text(text); //(todo 0.70.3) change to Text("")

    var icon = widget.control.get("icon");
    Color? iconColor = widget.control.getColor("icon_color", context);

    Widget? iconWidget = icon is Control
        ? ControlWidget(control: icon)
        : icon is String
            ? Icon(widget.control.getIcon("icon"), color: iconColor)
            : null;

    Widget child;
    if (iconWidget != null) {
      if (contentWidget != const Text("")) {
        child = Row(
          mainAxisSize: MainAxisSize.min,
          children: [iconWidget, const SizedBox(width: 8), contentWidget],
        );
      } else {
        child = iconWidget;
      }
    } else {
      child = contentWidget;
    }

    //var pressedOpacity = widget.control.getDouble("opacity_on_click", 0.4)!;
    //var minSize = widget.control.getDouble("min_size", 44.0)!;

    // var color = control.getColor("color", context);
    var alignment = widget.control.getAlignment("alignment", Alignment.center)!;
    var borderRadius = widget.control.getBorderRadius(
        "border_radius", const BorderRadius.all(Radius.circular(8.0)))!;

    var padding = widget.control.getPadding("padding");

    // var style = control.getButtonStyle("style", Theme.of(context),
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

    // if (color != null) {
    //   child = DefaultTextStyle(
    //       style: CupertinoTheme.of(context)
    //           .textTheme
    //           .textStyle
    //           .copyWith(color: color),
    //       child: child);
    // }
    var url = widget.control.getString("url", "")!;
    Function()? onPressed = !widget.control.disabled
        ? () {
            if (url != "") {
              openWebBrowser(url,
                  webWindowName: widget.control.getString("url_target"));
            }
            widget.control.triggerEvent("click");
          }
        : null;

    CupertinoButton? button = CupertinoButton(
      onPressed: onPressed,
      disabledColor: widget.control.getColor(
          "disabled_bgcolor", context, CupertinoColors.quaternarySystemFill)!,
      color: widget.control.getColor("bgcolor", context),
      padding: padding,
      borderRadius: borderRadius,
      pressedOpacity: widget.control.getDouble("opacity_on_click", 0.4)!,
      alignment: alignment,
      minSize: widget.control.getDouble("min_size"),
      autofocus: widget.control.getBool("autofocus", false)!,
      focusColor: widget.control.getColor("focus_color", context),
      // onLongPress: !control.disabled
      //     ? () {
      //         FletBackend.of(context)
      //             .triggerControlEvent(control, "long_press");
      //       }
      //     : null,
      focusNode: _focusNode,
      // onFocusChange: (focused) {
      //   widget.control.triggerEvent(focused ? "focus" : "blur");
      // },
      child: child,
    );

    return ConstrainedControl(control: widget.control, child: button);
  }
}
