import 'package:flet/src/utils/theme.dart';
import 'package:material_ui/material_ui.dart';
import 'package:flutter_test/flutter_test.dart';

Future<BuildContext> _pumpContext(WidgetTester tester) async {
  late BuildContext ctx;
  await tester.pumpWidget(Builder(builder: (context) {
    ctx = context;
    return const SizedBox();
  }));
  return ctx;
}

void main() {
  testWidgets("Default theme has neutral surfaces", (tester) async {
    final context = await _pumpContext(tester);

    final light = parseTheme(null, context, Brightness.light);
    expect(light.colorScheme.surface, const Color(0xFFFFFFFF));
    expect(light.colorScheme.surfaceContainer, const Color(0xFFF2F2F2));
    expect(light.scaffoldBackgroundColor, const Color(0xFFFFFFFF));

    final dark = parseTheme(null, context, Brightness.dark);
    expect(dark.colorScheme.surface, const Color(0xFF121212));
    expect(dark.colorScheme.surfaceContainer, const Color(0xFF202020));
    expect(dark.scaffoldBackgroundColor, const Color(0xFF121212));
  });

  testWidgets("Neutral surfaces keep seeded accents", (tester) async {
    final context = await _pumpContext(tester);

    for (final brightness in Brightness.values) {
      final seeded =
          ColorScheme.fromSeed(seedColor: Colors.green, brightness: brightness);
      final theme =
          parseTheme({"color_scheme_seed": "green"}, context, brightness);
      expect(theme.colorScheme.primary, seeded.primary);
      expect(theme.colorScheme.secondaryContainer, seeded.secondaryContainer);
      expect(theme.colorScheme.error, seeded.error);
    }
  });

  testWidgets("Tonal surfaces match Material 3 seeded scheme", (tester) async {
    final context = await _pumpContext(tester);

    for (final brightness in Brightness.values) {
      final expected =
          ThemeData(colorSchemeSeed: Colors.blue, brightness: brightness);
      final theme = parseTheme({"surfaces": "tonal"}, context, brightness);
      expect(theme.colorScheme.surface, expected.colorScheme.surface);
      expect(theme.colorScheme.surfaceContainer,
          expected.colorScheme.surfaceContainer);
      expect(theme.colorScheme.outline, expected.colorScheme.outline);
    }
  });

  testWidgets("Explicit color_scheme surface overrides neutral ramp",
      (tester) async {
    final context = await _pumpContext(tester);

    final theme = parseTheme({
      "color_scheme": {"surface": "#eeeeee"}
    }, context, Brightness.light);
    expect(theme.colorScheme.surface, const Color(0xFFEEEEEE));
    expect(theme.colorScheme.surfaceContainer, const Color(0xFFF2F2F2));
  });
}
