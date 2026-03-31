import 'dart:convert';

import 'package:flutter_code_editor/flutter_code_editor.dart' as fce;

class JsonLocalAnalyzer extends fce.AbstractAnalyzer {
  const JsonLocalAnalyzer();

  static const _defaultAnalyzer = fce.DefaultLocalAnalyzer();

  @override
  Future<fce.AnalysisResult> analyze(fce.Code code) async {
    final issues = (await _defaultAnalyzer.analyze(code)).issues.toList();

    if (code.text.trim().isEmpty) {
      return fce.AnalysisResult(issues: issues);
    }

    try {
      jsonDecode(code.text);
    } on FormatException catch (error) {
      issues.add(
        fce.Issue(
          line: _lineFromOffset(code.text, error.offset),
          message: error.message,
          type: fce.IssueType.error,
        ),
      );
    }

    return fce.AnalysisResult(issues: issues);
  }

  int _lineFromOffset(String text, int? offset) {
    final safeOffset = (offset ?? 0).clamp(0, text.length);
    return '\n'.allMatches(text.substring(0, safeOffset)).length;
  }
}
