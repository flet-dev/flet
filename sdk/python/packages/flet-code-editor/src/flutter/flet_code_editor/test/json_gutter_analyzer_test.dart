import 'package:flutter_code_editor/flutter_code_editor.dart' as fce;
import 'package:flutter_test/flutter_test.dart';

import 'package:flet_code_editor/src/utils/flet_code_controller.dart';

class TestAnalyzer extends fce.AbstractAnalyzer {
  const TestAnalyzer(this.issues);

  final List<fce.Issue> issues;

  @override
  Future<fce.AnalysisResult> analyze(fce.Code code) async {
    return fce.AnalysisResult(issues: issues);
  }
}

void main() {
  // ISSUE-6312: Regression coverage for Python-side analyzer integration.
  group('FletCodeController external analysis', () {
    test('uses analyzer results when external analysis is disabled', () async {
      final expectedIssue = fce.Issue(
        line: 1,
        message: 'syntax error',
        type: fce.IssueType.error,
      );
      final controller = FletCodeController(
        text: '{invalid}',
        analyzer: TestAnalyzer([expectedIssue]),
      );

      await controller.analyzeCode();

      expect(controller.analysisResult.issues, [expectedIssue]);
    });

    test('skips Dart-side analyzer when external analysis is enabled', () async {
      final controller = FletCodeController(
        text: '{invalid}',
        analyzer: TestAnalyzer([
          fce.Issue(
            line: 1,
            message: 'should be ignored',
            type: fce.IssueType.error,
          ),
        ]),
        externalAnalysisEnabled: true,
      );

      await controller.analyzeCode();

      expect(controller.analysisResult.issues, isEmpty);
    });

    test('applies issues returned from Python-side analysis', () {
      final controller = FletCodeController(
        text: '{\n  "name": "flet"\n  "version": 1\n}',
        externalAnalysisEnabled: true,
      );

      controller.setIssues([
        fce.Issue(
          line: 2,
          message: 'Missing comma',
          type: fce.IssueType.error,
        ),
      ]);

      expect(controller.analysisResult.issues, hasLength(1));
      expect(controller.analysisResult.issues.single.line, 2);
      expect(
        controller.analysisResult.issues.single.message,
        'Missing comma',
      );
    });
  });
}
