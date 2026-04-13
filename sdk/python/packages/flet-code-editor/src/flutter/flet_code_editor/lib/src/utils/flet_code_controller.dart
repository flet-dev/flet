import 'package:flutter/widgets.dart';
import 'package:flutter_code_editor/flutter_code_editor.dart' as fce;

class FletCodeController extends fce.CodeController {
  FletCodeController({
    super.text,
    super.language,
    this.externalAnalysisEnabled = false,
    fce.AbstractAnalyzer? analyzer,
  }) : super(analyzer: analyzer ?? const fce.DefaultLocalAnalyzer());

  bool autocompletionEnabled = false;
  final bool externalAnalysisEnabled;

  // ISSUE-6312: Allow Python-side analyzers to push issues back into the
  // controller instead of requiring a Dart-side analyzer per language.
  void setIssues(List<fce.Issue> issues) {
    if (_sameIssues(analysisResult.issues, issues)) {
      return;
    }
    analysisResult = fce.AnalysisResult(issues: issues);
    notifyListeners();
  }

  @override
  Future<void> analyzeCode() async {
    if (externalAnalysisEnabled) {
      return;
    }
    return super.analyzeCode();
  }

  bool _sameIssues(List<fce.Issue> left, List<fce.Issue> right) {
    if (identical(left, right)) {
      return true;
    }
    if (left.length != right.length) {
      return false;
    }
    for (var index = 0; index < left.length; index++) {
      final a = left[index];
      final b = right[index];
      if (a.line != b.line ||
          a.message != b.message ||
          a.type != b.type ||
          a.suggestion != b.suggestion ||
          a.url != b.url) {
        return false;
      }
    }
    return true;
  }

  @override
  Future<void> generateSuggestions() async {
    if (!autocompletionEnabled) {
      popupController.hide();
      return;
    }
    return super.generateSuggestions();
  }

  @override
  void insertSelectedWord() {
    final previousSelection = selection;
    final selectedWord = popupController.getSelectedWord();
    final startPosition = value.wordAtCursorStart;
    final currentWord = value.wordAtCursor;

    if (startPosition == null || currentWord == null) {
      popupController.hide();
      return;
    }

    final endReplacingPosition = startPosition + currentWord.length;
    final endSelectionPosition = startPosition + selectedWord.length;

    final replacedText = text.replaceRange(
      startPosition,
      endReplacingPosition,
      selectedWord,
    );

    final adjustedSelection = previousSelection.copyWith(
      baseOffset: endSelectionPosition,
      extentOffset: endSelectionPosition,
    );

    value = TextEditingValue(text: replacedText, selection: adjustedSelection);

    popupController.hide();
  }
}
