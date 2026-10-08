import 'package:flet/flet.dart';
import 'package:material_ui/material_ui.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

/// Builds the [ShadThemeData] described by a `flet_shadcn_ui.Theme` control.
///
/// When `brightness` is not set, the brightness of the enclosing Material
/// theme is used, so the scheme follows the page's light/dark mode.
ShadThemeData parseShadThemeData(Control control, BuildContext context) {
  final brightness =
      control.getBrightness("brightness") ?? Theme.of(context).brightness;
  return ShadThemeData(
    brightness: brightness,
    colorScheme: ShadColorScheme.fromName(
      control.getString("color_scheme", "slate")!,
      brightness: brightness,
    ),
    radius: control.getBorderRadius("radius"),
  );
}

/// Wraps [child] in a default [ShadTheme] if [context] has none.
///
/// Every Shadcn widget looks up [ShadTheme.of] and throws without one, and
/// Flet has no way to put a [ShadTheme] above the page, so each control
/// provides a slate theme matching the page brightness as a fallback.
Widget withShadTheme(BuildContext context, Widget child) {
  if (ShadTheme.maybeOf(context) != null) return child;
  final brightness = Theme.of(context).brightness;
  return ShadTheme(
    data: ShadThemeData(
      brightness: brightness,
      colorScheme: ShadColorScheme.fromName("slate", brightness: brightness),
    ),
    child: child,
  );
}

/// Builds shadcn_ui's text field context menu inside the field's [ShadTheme].
///
/// Flutter shows the menu in the root overlay, which doesn't inherit themes
/// from the field's context, and Flet has no [ShadTheme] above the root
/// overlay, so shadcn_ui's default menu would throw looking for one.
Widget shadContextMenuBuilder(BuildContext context, EditableTextState state) {
  return ShadTheme(
    data: ShadTheme.of(state.context, listen: false),
    child: ShadInputState.defaultContextMenuBuilder(context, state),
  );
}

/// Turns off the native context menu of the text fields inside [child].
///
/// For Shadcn widgets that don't take a `contextMenuBuilder` (InputOTP,
/// TimePicker): their default menu would throw for the reason described in
/// [shadContextMenuBuilder].
Widget withoutShadContextMenu(Widget child) {
  return Builder(
    builder: (context) {
      final theme = ShadTheme.of(context);
      return ShadTheme(
        data: theme.copyWith(
          inputTheme: theme.inputTheme.copyWith(useBrowserContextMenu: true),
        ),
        child: child,
      );
    },
  );
}

/// Gives [child] the theme's muted foreground color.
///
/// shadcn_ui's `muted` text style has no color; most widgets add one, but
/// some (the ShadRadio sublabel, ShadContextMenuItem trailing text) use it as
/// is, and Flutter paints color-less text white. Wrap those children with this.
Widget? withMutedColor(BuildContext context, Widget? child) {
  if (child == null) return null;
  return DefaultTextStyle.merge(
    style: TextStyle(color: ShadTheme.of(context).colorScheme.mutedForeground),
    child: child,
  );
}
