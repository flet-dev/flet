import 'package:flutter/cupertino.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/launch_url.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';
import 'control_widget.dart';

class CupertinoButtonControl extends StatelessWidget {
  final Control control;

  const CupertinoButtonControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoButton build: ${control.id}");
    // var theme = Theme.of(context);
    String text = control.getString("text", "")!; // to be removed in 0.70.3
    var content = control.get("content");
    // var icon = control.getIcon("icon");
    // var iconColor = control.getColor("icon_color", context);

    // // IconButton props below
    // var iconSize = control.getDouble("icon_size");
    // var selected = control.getBool("selected", false)!;
    // var selectedIcon = control.getIcon("selected_icon");
    // var selectedIconColor = control.getColor("selected_icon_color", context);

    Widget contentWidget = content is Control
        ? ControlWidget(control: content)
        : content is String
            ? Text(content)
            : Text(text); // to be changed to Text("") in 0.70.3

    // Widget? child;
    // List<Widget> children = [];
    // if (icon != null) {
    //   children.add(Icon(
    //     selected ? selectedIcon : icon,
    //     color: selected
    //         ? selectedIconColor
    //         : control.disabled
    //             ? theme.disabledColor
    //             : iconColor,
    //     size: iconSize,
    //   ));
    // }
    // children.add(contentWidget);
    // Widget? iconWidget = icon != null
    //     ? Icon(
    //         selected ? selectedIcon : icon,
    //         color: selected
    //             ? selectedIconColor
    //             : control.disabled
    //                 ? theme.disabledColor
    //                 : iconColor,
    //         size: iconSize,
    //       )
    //     : null;
    // children.add(iconWidget);
    // Widget child;
    // if (children.length == 2) {
    //   children.insert(1, const SizedBox(width: 8));
    //   child = Row(
    //     mainAxisSize: MainAxisSize.min,
    //     children: children,
    //   );
    // } else {
    //   child = children.first;
    // }

    // var pressedOpacity = control.getDouble("opacity_on_click")!;
    // var minSize = control.getDouble("min_size", 44.0)!;
    var url = control.getString("url", "")!;
    var disabledColor = control.getColor(
        "disabled_bgcolor", context, CupertinoColors.quaternarySystemFill)!;
    var bgColor = control.getColor("bgcolor", context);
    // var color = control.getColor("color", context);
    // var alignment = control.getAlignment("alignment", Alignment.center)!;
    // var borderRadius = control.getBorderRadius(
    //     "borderRadius", const BorderRadius.all(Radius.circular(8.0)))!;

    // var padding = control.getPadding("padding");

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

    Function()? onPressed = !control.disabled
        ? () {
            if (url != "") {
              openWebBrowser(url,
                  webWindowName: control.getString("url_target"));
            }
            control.triggerEvent("click");
          }
        : null;

    CupertinoButton? button = CupertinoButton(
      onPressed: onPressed,
      disabledColor: disabledColor,
      color: bgColor,
      //padding: padding,
      //borderRadius: borderRadius,
      //pressedOpacity: pressedOpacity,
      //alignment: alignment,
      //minSize: minSize,
      //autofocus: control.getBool("autofocus", false)!,
      //focusColor: control.getColor("focus_color", context),
      // onLongPress: !control.disabled
      //     ? () {
      //         FletBackend.of(context)
      //             .triggerControlEvent(control, "long_press");
      //       }
      //     : null,
      // onFocusChange: (focused) {
      //   FletBackend.of(context)
      //       .triggerControlEvent(control, focused ? "focus" : "blur");
      // },
      //child: child,
      child: contentWidget,
      //child: const Text("OK")
    );

    return ConstrainedControl(control: control, child: button);
  }
}
