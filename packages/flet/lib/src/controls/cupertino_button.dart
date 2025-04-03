import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

//import '../flet_control_backend.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/buttons.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import '../widgets/error.dart';
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
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoButton build: ${widget.control.id}");
    bool disabled = widget.control.disabled || widget.control.parent!.disabled;
    var theme = Theme.of(context);

    Control? content = widget.control.child("content");

    String? text = widget.control.getString("text");
    IconData? icon = parseIcon(widget.control.getString("icon"));
    Color? iconColor = widget.control.getColor("icon_color", context);

    // IconButton props below
    double? iconSize = widget.control.getDouble("icon_size");
    bool selected = widget.control.getBool("selected", false)!;
    IconData? selectedIcon =
        parseIcon(widget.control.getString("selected_icon"));
    Color? selectedIconColor =
        widget.control.getColor("selected_icon_color", context);

    Widget? child;
    List<Widget> children = [];
    if (icon != null) {
      children.add(Icon(
        selected ? selectedIcon : icon,
        color: selected
            ? selectedIconColor
            : disabled
                ? theme.disabledColor
                : iconColor,
        size: iconSize,
      ));
    }
    if (text != null) {
      children.add(Text(text));
    }

    if (content is Control) {
      child = ControlWidget(control: content);
    } else if (children.isNotEmpty) {
      if (children.length == 2) {
        children.insert(1, const SizedBox(width: 8));
        child = Row(
          mainAxisSize: MainAxisSize.min,
          children: children,
        );
      } else {
        child = children.first;
      }
    }

    if (child == null) {
      return const ErrorControl(
        "CupertinoButton has nothing to display",
        description: "Provide at minimum text or (visible) content",
      );
    }

    double pressedOpacity = widget.control.getDouble("opacity_on_click")!;
    double minSize = widget.control.getDouble("min_size", 44.0)!;
    String url = widget.control.getString("url", "")!;
    Color disabledColor =
        widget.control.getColor("disabled_bgcolor", context) ??
            CupertinoColors.quaternarySystemFill;
    Color? bgColor = widget.control.getColor("bgColor", context);
    Color? color = widget.control.getColor("color", context);
    AlignmentGeometry alignment =
        parseAlignment(widget.control, "alignment", Alignment.center)!;
    BorderRadius borderRadius = parseBorderRadius(widget.control,
        "borderRadius", const BorderRadius.all(Radius.circular(8.0)))!;

    EdgeInsets? padding = parseEdgeInsets(widget.control, "padding");

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

    if (style != null) {
      Set<WidgetState> widgetStates = selected ? {WidgetState.selected} : {};

      // Check if the widget is disabled and update the foregroundColor accordingly
      // backgroundColor is not updated here, as it is handled by disabledColor
      if (disabled) {
        style = style.copyWith(
          foregroundColor: WidgetStatePropertyAll(theme.disabledColor),
        );
      }

      // Resolve color, background color, and padding based on widget states
      color = style.foregroundColor?.resolve(widgetStates);
      bgColor = style.backgroundColor?.resolve(widgetStates);
      padding = style.padding?.resolve({}) as EdgeInsets?;
    }

    if (color != null) {
      child = DefaultTextStyle(
          style: CupertinoTheme.of(context)
              .textTheme
              .textStyle
              .copyWith(color: color),
          child: child);
    }

    Function()? onPressed = !disabled
        ? () {
            debugPrint("CupertinoButton ${widget.control.id} clicked!");
            if (url != "") {
              openWebBrowser(url,
                  webWindowName: widget.control.getString("url_target"));
            }
            FletBackend.of(context)
                .triggerControlEvent(widget.control, "click");
          }
        : null;

    CupertinoButton? button = CupertinoButton(
      onPressed: onPressed,
      disabledColor: disabledColor,
      color: bgColor,
      padding: padding,
      borderRadius: borderRadius,
      pressedOpacity: pressedOpacity,
      alignment: alignment,
      minSize: minSize,
      onLongPress: !disabled
          ? () {
              FletBackend.of(context)
                  .triggerControlEvent(widget.control, "long_press");
            }
          : null,
      onFocusChange: (focused) {
        FletBackend.of(context)
            .triggerControlEvent(widget.control, focused ? "focus" : "blur");
      },
      child: child,
    );

    return ConstrainedControl(control: widget.control, child: button);
  }
}
