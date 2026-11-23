import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

/// A `flet_fluent_ui.Button`, `FilledButton`, `OutlinedButton`,
/// `HyperlinkButton` or `IconButton`, picked by the control type.
class FluentButtonControl extends StatefulWidget {
  final Control control;

  const FluentButtonControl({super.key, required this.control});

  @override
  State<FluentButtonControl> createState() => _FluentButtonControlState();
}

class _FluentButtonControlState extends State<FluentButtonControl> {
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
    widget.control.removeInvokeMethodListener(_invokeMethod);
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("${widget.control.type}.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown ${widget.control.type} method: $name");
    }
  }

  void _onFocusChange() {
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  Widget build(BuildContext context) {
    final control = widget.control;
    debugPrint("${control.type} build: ${control.id}");

    final onPressed =
        control.disabled ? null : () => control.triggerEvent("click");
    final onLongPress = !control.disabled && control.hasEventHandler("long_press")
        ? () => control.triggerEvent("long_press")
        : null;
    final autofocus = control.getBool("autofocus", false)!;
    final child = control.buildTextOrWidget("content") ?? const SizedBox.shrink();

    final Widget button = switch (control.type) {
      "FluentFilledButton" => FilledButton(
          onPressed: onPressed,
          onLongPress: onLongPress,
          focusNode: _focusNode,
          autofocus: autofocus,
          child: child,
        ),
      "FluentOutlinedButton" => OutlinedButton(
          onPressed: onPressed,
          onLongPress: onLongPress,
          focusNode: _focusNode,
          autofocus: autofocus,
          child: child,
        ),
      "FluentHyperlinkButton" => HyperlinkButton(
          onPressed: onPressed,
          onLongPress: onLongPress,
          focusNode: _focusNode,
          autofocus: autofocus,
          child: child,
        ),
      "FluentIconButton" => IconButton(
          onPressed: onPressed,
          onLongPress: onLongPress,
          focusNode: _focusNode,
          autofocus: autofocus,
          icon: control.get("icon") is int
              ? Icon(
                  control.getIconData("icon"),
                  size: control.getDouble("icon_size"),
                )
              : control.buildIconOrWidget("icon") ?? const SizedBox.shrink(),
        ),
      _ => Button(
          onPressed: onPressed,
          onLongPress: onLongPress,
          focusNode: _focusNode,
          autofocus: autofocus,
          child: child,
        ),
    };

    return LayoutControl(
      control: control,
      child: withFluentTheme(context, button),
    );
  }
}
