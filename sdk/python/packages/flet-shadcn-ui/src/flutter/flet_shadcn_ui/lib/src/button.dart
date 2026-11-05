import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/icons.dart';
import 'utils/theme.dart';

class ShadButtonControl extends StatefulWidget {
  final Control control;

  const ShadButtonControl({super.key, required this.control});

  @override
  State<ShadButtonControl> createState() => _ShadButtonControlState();
}

class _ShadButtonControlState extends State<ShadButtonControl> {
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
    debugPrint("ShadButton.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown ShadButton method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadButton build: ${widget.control.id}");

    final control = widget.control;
    final button = ShadButton.raw(
      variant: parseEnum(ShadButtonVariant.values, control.getString("variant"),
          ShadButtonVariant.primary)!,
      size: parseEnum(ShadButtonSize.values, control.getString("size"),
          ShadButtonSize.regular)!,
      focusNode: _focusNode,
      enabled: !control.disabled,
      autofocus: control.getBool("autofocus", false)!,
      leading: buildShadIconOrWidget(control, "leading"),
      trailing: buildShadIconOrWidget(control, "trailing"),
      backgroundColor: control.getColor("bgcolor", context),
      hoverBackgroundColor: control.getColor("hover_bgcolor", context),
      foregroundColor: control.getColor("color", context),
      hoverForegroundColor: control.getColor("hover_color", context),
      gap: control.getDouble("gap"),
      onPressed: () => control.triggerEvent("click"),
      onLongPress: control.hasEventHandler("long_press")
          ? () => control.triggerEvent("long_press")
          : null,
      onHoverChange: control.hasEventHandler("hover")
          ? (value) => control.triggerEvent("hover", value)
          : null,
      onFocusChange: (focused) =>
          control.triggerEvent(focused ? "focus" : "blur"),
      child: control.buildTextOrWidget("content"),
    );

    return LayoutControl(
        control: control, child: withShadTheme(context, button));
  }
}
