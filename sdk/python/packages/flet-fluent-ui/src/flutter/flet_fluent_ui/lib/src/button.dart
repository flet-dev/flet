import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

/// Greys out the text and border of a disabled OutlinedButton.
///
/// fluent_ui's OutlinedButton keeps its enabled text and border colors when
/// disabled, so it can't be told apart from an enabled one. The enabled
/// colors here are fluent_ui's own.
ButtonStyle _outlinedButtonStyle(BuildContext context) {
  return ButtonStyle(
    foregroundColor: WidgetStateProperty.resolveWith((states) {
      final theme = FluentTheme.of(context);
      return states.isDisabled
          ? theme.resources.textFillColorDisabled
          : theme.inactiveColor;
    }),
    shape: WidgetStateProperty.resolveWith((states) {
      final theme = FluentTheme.of(context);
      return RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(2),
        side: BorderSide(
          color: states.isDisabled
              ? theme.resources.controlStrokeColorDefault
              : theme.inactiveColor,
        ),
      );
    }),
  );
}

/// Greys out the text of a disabled HyperlinkButton.
///
/// fluent_ui colors disabled hyperlink text with a fill color that is almost
/// invisible on the page background. The other states are fluent_ui's own.
ButtonStyle _hyperlinkButtonStyle(BuildContext context) {
  return ButtonStyle(
    foregroundColor: WidgetStateProperty.resolveWith((states) {
      final theme = FluentTheme.of(context);
      if (states.isDisabled) {
        return theme.resources.textFillColorDisabled;
      } else if (states.isPressed) {
        return theme.accentColor.tertiaryBrushFor(theme.brightness);
      } else if (states.isHovered) {
        return theme.accentColor.secondaryBrushFor(theme.brightness);
      }
      return theme.accentColor.defaultBrushFor(theme.brightness);
    }),
  );
}

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
      // The Builder's context is below the FluentTheme added by
      // withFluentTheme, which the style reads.
      "FluentOutlinedButton" => Builder(
          builder: (context) => OutlinedButton(
            onPressed: onPressed,
            onLongPress: onLongPress,
            focusNode: _focusNode,
            autofocus: autofocus,
            style: _outlinedButtonStyle(context),
            child: child,
          ),
        ),
      "FluentHyperlinkButton" => Builder(
          builder: (context) => HyperlinkButton(
            onPressed: onPressed,
            onLongPress: onLongPress,
            focusNode: _focusNode,
            autofocus: autofocus,
            style: _hyperlinkButtonStyle(context),
            child: child,
          ),
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
