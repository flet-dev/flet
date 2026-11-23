import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';
import 'package:material_ui/material_ui.dart' show Theme;

/// Builds the [FluentThemeData] described by a `flet_fluent_ui.Theme` control.
///
/// When `brightness` is not set, the brightness of the enclosing Material
/// theme is used, so the theme follows the page's light/dark mode.
FluentThemeData parseFluentThemeData(Control control, BuildContext context) {
  return FluentThemeData(
    brightness:
        control.getBrightness("brightness") ?? Theme.of(context).brightness,
    accentColor: control.getColor("accent_color", context)?.toAccentColor(),
    fontFamily: control.getString("font_family"),
  );
}

// FluentThemeData's factory derives a few hundred colors, so the fallback
// themes are built once per brightness.
final _fallbackThemes = <Brightness, FluentThemeData>{};

/// Wraps [child] in a default [FluentTheme] and [FluentLocalizations] if
/// [context] has none.
///
/// Fluent widgets look up [FluentTheme.of] and [FluentLocalizations.of] and
/// throw without them. Flet has no way to put either above the page, so each
/// control provides a blue-accented theme matching the page brightness and the
/// Fluent localizations for the app's locale as a fallback.
Widget withFluentTheme(BuildContext context, Widget child) {
  var result = child;
  if (FluentTheme.maybeOf(context) == null) {
    final brightness = Theme.of(context).brightness;
    result = FluentTheme(
      data: _fallbackThemes[brightness] ??=
          FluentThemeData(brightness: brightness),
      child: result,
    );
  }
  if (Localizations.of<FluentLocalizations>(context, FluentLocalizations) ==
      null) {
    result = Localizations.override(
      context: context,
      delegates: const [_FluentLocalizationsDelegate()],
      child: result,
    );
  }
  return result;
}

/// Loads [FluentLocalizations] for any locale, falling back to English for
/// locales fluent_ui has no translations for, so a Fluent control never finds
/// its localizations missing.
class _FluentLocalizationsDelegate
    extends LocalizationsDelegate<FluentLocalizations> {
  const _FluentLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) => true;

  @override
  Future<FluentLocalizations> load(Locale locale) =>
      FluentLocalizations.delegate.load(
        FluentLocalizations.delegate.isSupported(locale)
            ? locale
            : const Locale("en"),
      );

  @override
  bool shouldReload(_FluentLocalizationsDelegate old) => false;
}
