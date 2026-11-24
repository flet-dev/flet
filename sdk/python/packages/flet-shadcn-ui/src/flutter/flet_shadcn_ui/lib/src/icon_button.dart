import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadIconButtonControl extends StatefulWidget {
  final Control control;

  const ShadIconButtonControl({super.key, required this.control});

  @override
  State<ShadIconButtonControl> createState() => _ShadIconButtonControlState();
}

class _ShadIconButtonControlState extends State<ShadIconButtonControl> {
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    _focusNode.dispose();
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("ShadIconButton.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown ShadIconButton method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadIconButton build: ${widget.control.id}");

    final control = widget.control;
    var variant = parseEnum(ShadButtonVariant.values,
        control.getString("variant"), ShadButtonVariant.primary)!;
    if (variant == ShadButtonVariant.link) {
      variant = ShadButtonVariant.primary;
    }

    final button = ShadIconButton.raw(
      variant: variant,
      icon: control.buildIconOrWidget("icon", required: true)!,
      iconSize: control.getDouble("icon_size", 16),
      focusNode: _focusNode,
      enabled: !control.disabled,
      autofocus: control.getBool("autofocus", false)!,
      backgroundColor: control.getColor("bgcolor", context),
      hoverBackgroundColor: control.getColor("hover_bgcolor", context),
      foregroundColor: control.getColor("color", context),
      hoverForegroundColor: control.getColor("hover_color", context),
      onPressed: () => control.triggerEvent("click"),
      onLongPress: control.hasEventHandler("long_press")
          ? () => control.triggerEvent("long_press")
          : null,
      onHoverChange: control.hasEventHandler("hover")
          ? (value) => control.triggerEvent("hover", value)
          : null,
      onFocusChange: (focused) =>
          control.triggerEvent(focused ? "focus" : "blur"),
    );

    return LayoutControl(
        control: control, child: withShadTheme(context, button));
  }
}
