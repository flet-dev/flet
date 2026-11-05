import 'package:flet/src/controls/markdown.dart';
import 'package:flet/src/flet_backend.dart';
import 'package:flet/src/models/control.dart';
import 'package:flet/src/utils/theme.dart';
import 'package:flutter_markdown_plus/flutter_markdown_plus.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';

Iterable<Color?> _linkColors(InlineSpan span, [TextStyle? inherited]) sync* {
  if (span is TextSpan) {
    final style = inherited?.merge(span.style) ?? span.style;
    if (span.text == 'Flet') yield style?.color;
    for (final child in span.children ?? <InlineSpan>[]) {
      yield* _linkColors(child, style);
    }
  }
}

void main() {
  for (final brightness in Brightness.values) {
    for (final scenario in ['default', 'unrelated style', 'theme', 'control']) {
      testWidgets('Markdown colors follow $scenario styles in $brightness', (
        tester,
      ) async {
        final backend = FletBackend(
          pageUri: Uri.parse('http://localhost'),
          assetsDir: '',
          extensions: [],
          multiView: false,
        );
        addTearDown(backend.dispose);
        final hasTheme = scenario == 'theme' || scenario == 'control';
        final theme = ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.green,
            brightness: brightness,
          ),
          extensions: [
            if (hasTheme)
              const MarkdownTheme({
                'a_text_style': {'color': '#ff9800'},
                'p_text_style': {'size': 21.0},
              }),
          ],
        );
        final control = Control(
          id: 1,
          type: 'Markdown',
          properties: {
            'value': '[Flet](https://flet.dev)\n\n> A quote',
            if (scenario == 'unrelated style')
              'md_style_sheet': {
                'p_text_style': {'size': 19.0},
              },
            if (scenario == 'control')
              'md_style_sheet': {
                'a_text_style': {'color': '#e91e63'},
              },
          },
          backend: backend,
        );

        await tester.pumpWidget(
          MaterialApp(
            theme: theme,
            home: Scaffold(body: MarkdownControl(control: control)),
          ),
        );
        expect(tester.takeException(), isNull);

        final expectedColor = scenario == 'control'
            ? const Color(0xffe91e63)
            : hasTheme
            ? const Color(0xffff9800)
            : theme.colorScheme.primary;
        final body = tester.widget<MarkdownBody>(find.byType(MarkdownBody));
        final links = tester
            .widgetList<RichText>(
              find.descendant(
                of: find.byType(MarkdownBody),
                matching: find.byType(RichText),
              ),
            )
            .expand((text) => _linkColors(text.text));
        expect(links, isNotEmpty);
        expect(links, everyElement(expectedColor));
        expect(body.styleSheet!.a!.color, expectedColor);
        expect(
          (body.styleSheet!.blockquoteDecoration as BoxDecoration).color,
          theme.colorScheme.surfaceContainerHigh,
        );
        if (hasTheme) expect(body.styleSheet!.p!.fontSize, 21.0);
      });
    }
  }
}
