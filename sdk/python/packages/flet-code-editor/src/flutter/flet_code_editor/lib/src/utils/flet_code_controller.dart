import 'package:flutter/widgets.dart';
import 'package:flutter_code_editor/flutter_code_editor.dart' as fce;

class FletCodeController extends fce.CodeController {
  FletCodeController({
    super.text,
    super.language,
  });

  bool autocompletionEnabled = false;

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

    value = TextEditingValue(
      text: replacedText,
      selection: adjustedSelection,
    );

    popupController.hide();
  }
}
