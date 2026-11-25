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

FluentThemeData _fallbackTheme(Brightness brightness) =>
    _fallbackThemes[brightness] ??= FluentThemeData(brightness: brightness);

/// Provides a default [FluentTheme] and [FluentLocalizations] to the whole
/// app, from `Extension.wrapApp`.
///
/// Fluent popups (picker lists, flyouts) open on the app's navigator, above
/// any control, and look the theme up there. The theme matches the page
/// brightness.
///
/// [FluentTheme] also sets a text style and an icon theme for its
/// descendants. The text style stays: at this level, the app has only
/// Flutter's fallback style (pages and Material dialogs set their own), and
/// Fluent popups need Fluent's. The icon theme is reset to the app's, which
/// is the one Flet's own controls use.
Widget wrapAppWithFluentTheme(BuildContext context, Widget child) {
  return Localizations.override(
    context: context,
    delegates: const [_FluentLocalizationsDelegate()],
    child: FluentTheme(
      data: _fallbackTheme(Theme.of(context).brightness),
      child: IconTheme(data: IconTheme.of(context), child: child),
    ),
  );
}

/// Wraps [child] in a default [FluentTheme] and [FluentLocalizations] unless
/// a `flet_fluent_ui.Theme` (or another Fluent theme) is above it.
///
/// Fluent widgets look up [FluentTheme.of] and [FluentLocalizations.of] and
/// throw without them. A control outside a `Theme` gets a blue-accented theme
/// matching the brightness of the enclosing Material theme (which can differ
/// from the page's, see [wrapAppWithFluentTheme]), along with the Fluent
/// text style and icon theme.
Widget withFluentTheme(BuildContext context, Widget child) {
  var result = child;
  final theme = FluentTheme.maybeOf(context);
  if (theme == null || _fallbackThemes.values.any((t) => identical(t, theme))) {
    result = FluentTheme(
      data: _fallbackTheme(Theme.of(context).brightness),
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
