import 'package:flutter_code_editor/flutter_code_editor.dart' as fce;
import 'package:flutter_test/flutter_test.dart';
import 'package:highlight/languages/json.dart';

import 'package:flet_code_editor/src/utils/flet_code_controller.dart';
import 'package:flet_code_editor/src/utils/json_analyzer.dart';

void main() {
  group('FletCodeController JSON analyzer', () {
    test('uses JSON analyzer for JSON language', () {
      final controller = FletCodeController(
        text: '{"name": "flet"}',
        language: json,
      );

      expect(controller.analyzer, isA<JsonLocalAnalyzer>());
    });

    test('reports invalid JSON syntax as gutter issues', () async {
      final controller = FletCodeController(
        text: '{\n  "name": "flet"\n  "version": 1\n}',
        language: json,
      );

      await controller.analyzeCode();

      expect(controller.analysisResult.issues, hasLength(1));
      expect(controller.analysisResult.issues.single.line, 2);
      expect(controller.analysisResult.issues.single.type, fce.IssueType.error);
    });

    test('keeps valid JSON free of issues', () async {
      final controller = FletCodeController(
        text: '{\n  "name": "flet",\n  "version": 1\n}',
        language: json,
      );

      await controller.analyzeCode();

      expect(controller.analysisResult.issues, isEmpty);
    });
  });
}
