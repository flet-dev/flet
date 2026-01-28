import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_code_editor/flutter_code_editor.dart' as fce;
import 'package:flutter_highlight/theme_map.dart';
import 'package:highlight/languages/all.dart';

class CodeEditorControl extends StatefulWidget {
  final Control control;

  const CodeEditorControl({super.key, required this.control});

  @override
  State<CodeEditorControl> createState() => _CodeEditorControlState();
}

class _CodeEditorControlState extends State<CodeEditorControl> {
  late _FletCodeController _controller;
  late final FocusNode _focusNode;
  TextSelection? _selection;
  String _text = "";
  String? _fullText;
  String? _languageName;
  List<String>? _readOnlySectionNames;
  List<String>? _visibleSectionNames;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
    _controller = _createController();
    _controller.addListener(_handleControllerChange);
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    _controller.removeListener(_handleControllerChange);
    _controller.dispose();
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("CodeEditor.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
        break;
      case "fold_comment_at_line_zero":
        (_controller as dynamic).foldCommentAtLineZero();
        break;
      case "fold_imports":
        (_controller as dynamic).foldImports();
        break;
      case "fold_outside_sections":
        final sections = _stringList(args["section_names"]);
        (_controller as dynamic).foldOutsideSections(sections ?? []);
        break;
      case "fold_at":
        final line = parseInt(args["line_number"]);
        if (line != null) {
          (_controller as dynamic).foldAt(line);
        }
        break;
      default:
        throw Exception("Unknown CodeEditor method: $name");
    }
  }

  void _onFocusChange() {
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  _FletCodeController _createController() {
    _languageName = _resolveLanguageName();
    _readOnlySectionNames = _readSectionNames(
      "read_only_section_names",
      fallback: "read_only_section_mames",
    );
    _visibleSectionNames =
        _stringList(widget.control.get("visible_section_names"));

    final initialText = _initialTextFromControl();
    final language = _languageName != null
        ? allLanguages[_languageName!.toLowerCase()]
        : null;
    final namedSectionParser = _buildNamedSectionParser(_readOnlySectionNames);

    return _FletCodeController(
      text: initialText,
      language: language,
      namedSectionParser: namedSectionParser,
      readOnlySectionNames: _readOnlySectionNames?.toSet() ?? const {},
      visibleSectionNames: _visibleSectionNames?.toSet() ?? const {},
    );
  }

  String _initialTextFromControl() {
    final value = widget.control.get("value");
    if (value is Map && value["text"] != null) {
      return value["text"].toString();
    }
    return widget.control.getString("full_text") ??
        widget.control.getString("text") ??
        "";
  }

  String? _resolveLanguageName() {
    final language = widget.control.get("language");
    if (language is String) {
      return language;
    }
    return null;
  }

  fce.AbstractNamedSectionParser? _buildNamedSectionParser(
    List<String>? readOnlySectionNames,
  ) {
    if (readOnlySectionNames == null) {
      return null;
    }
    return const fce.BracketsStartEndNamedSectionParser();
  }

  List<String>? _stringList(dynamic value) {
    if (value is List) {
      return value.map((e) => e.toString()).toList();
    }
    return null;
  }

  List<String>? _readSectionNames(String primary, {String? fallback}) {
    final primaryValue = _stringList(widget.control.get(primary));
    if (primaryValue != null) {
      return primaryValue;
    }
    if (fallback == null) {
      return null;
    }
    return _stringList(widget.control.get(fallback));
  }

  String _readFullText() => _controller.fullText;

  void _setFullText(String value) {
    _controller.fullText = value;
  }

  void _handleControllerChange() {
    final text = _controller.text;
    final selection = _controller.selection;
    final selectionChanged = selection != _selection;
    final textChanged = text != _text;

    if (!textChanged && !selectionChanged) {
      return;
    }

    _text = text;
    _selection = selection;
    _fullText = _readFullText();

    final updates = <String, dynamic>{};

    if (textChanged) {
      updates["text"] = text;
      updates["full_text"] = _fullText;
    }

    if (textChanged || selectionChanged) {
      final value = <String, dynamic>{"text": text};
      if (selection.isValid) {
        value["selection"] = selection.toMap();
      }
      updates["value"] = value;
    }

    if (updates.isNotEmpty) {
      widget.control.updateProperties(updates);
    }

    if (textChanged && widget.control.getBool("on_change", false)!) {
      widget.control.triggerEvent("change", text);
    }

    if (selectionChanged &&
        selection.isValid &&
        widget.control.getBool("on_selection_change", false)!) {
      widget.control.triggerEvent("selection_change", {
        "selected_text": text.substring(selection.start, selection.end),
        "selection": selection.toMap(),
      });
    }
  }

  fce.CodeThemeData? _buildThemeData(BuildContext context) {
    final codeTheme = widget.control.get("code_theme");
    if (codeTheme is! Map) {
      if (codeTheme is String) {
        final named = themeMap[codeTheme.toLowerCase()];
        return named == null ? null : fce.CodeThemeData(styles: named);
      }
      return null;
    }
    final themeName = codeTheme["name"];
    if (themeName is String) {
      final named = themeMap[themeName.toLowerCase()];
      if (named != null) {
        return fce.CodeThemeData(styles: named);
      }
    }
    final styles = codeTheme["styles"];
    if (styles is! Map) {
      return null;
    }

    final parsedStyles = <String, TextStyle>{};
    styles.forEach((key, value) {
      final style = parseTextStyle(value, Theme.of(context));
      if (style != null) {
        parsedStyles[key.toString()] = style;
      }
    });

    if (parsedStyles.isEmpty) {
      return null;
    }

    return fce.CodeThemeData(styles: parsedStyles);
  }

  fce.GutterStyle? _buildGutterStyle(BuildContext context) {
    final gutterStyle = widget.control.get("gutter_style");
    if (gutterStyle is! Map) {
      return null;
    }

    final textStyle =
        parseTextStyle(gutterStyle["text_style"], Theme.of(context));
    final background =
        parseColor(gutterStyle["background_color"], Theme.of(context));
    final width = parseDouble(gutterStyle["width"]);
    final margin = _parseGutterMargin(gutterStyle["margin"]);

    final showErrors = gutterStyle["show_errors"];
    final showFoldingHandles = gutterStyle["show_folding_handles"];
    final showLineNumbers = gutterStyle["show_line_numbers"];

    return fce.GutterStyle(
      textStyle: textStyle,
      background: background,
      width: width ?? 80.0,
      margin: margin ?? 10.0,
      showErrors: showErrors is bool ? showErrors : true,
      showFoldingHandles:
          showFoldingHandles is bool ? showFoldingHandles : true,
      showLineNumbers: showLineNumbers is bool ? showLineNumbers : true,
    );
  }

  double? _parseGutterMargin(dynamic value) {
    final margin = parseDouble(value);
    if (margin != null) {
      return margin;
    }
    final edgeInsets = parseEdgeInsets(value);
    if (edgeInsets == null) {
      return null;
    }
    return (edgeInsets.left + edgeInsets.right) / 2;
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CodeEditor build: ${widget.control.id}");

    final languageName = _resolveLanguageName();
    final readOnlySectionNames = _readSectionNames(
      "read_only_section_names",
      fallback: "read_only_section_mames",
    );
    final visibleSectionNames =
        _stringList(widget.control.get("visible_section_names"));

    if (languageName != _languageName ||
        !_listEquals(readOnlySectionNames, _readOnlySectionNames) ||
        !_listEquals(visibleSectionNames, _visibleSectionNames)) {
      final previousSelection = _controller.selection;
      _controller.removeListener(_handleControllerChange);
      _controller.dispose();
      _languageName = languageName;
      _readOnlySectionNames = readOnlySectionNames;
      _visibleSectionNames = visibleSectionNames;
      _controller = _createController();
      _controller.addListener(_handleControllerChange);
      if (previousSelection.isValid) {
        _controller.selection = previousSelection;
      }
    }

    final value = widget.control.get("value");
    if (value is Map) {
      final valueText = value["text"]?.toString() ?? "";
      if (valueText != _controller.text) {
        _controller.value = TextEditingValue(
          text: valueText,
          selection: TextSelection.collapsed(offset: valueText.length),
        );
      }
      final selection = parseTextSelection(
        value["selection"],
        minOffset: 0,
        maxOffset: valueText.length,
      );
      if (selection != null && selection != _controller.selection) {
        _controller.selection = selection;
      }
    } else {
      final fullText = widget.control.getString("full_text");
      if (fullText != null && fullText != _fullText) {
        _fullText = fullText;
        _setFullText(fullText);
      } else {
        final text = widget.control.getString("text");
        if (text != null && text != _controller.text) {
          _controller.value = TextEditingValue(
            text: text,
            selection: TextSelection.collapsed(offset: text.length),
          );
        }
      }
    }

    final themeData = _buildThemeData(context);
    final gutterStyle = _buildGutterStyle(context);
    final textStyle = parseTextStyle(
      widget.control.get("text_style"),
      Theme.of(context),
    );
    final autocompletionEnabled =
        widget.control.getBool("autocompletion_enabled", false)!;
    final autocompletionWords =
        _stringList(widget.control.get("autocompletion_words")) ?? const [];
    _controller.autocompletionEnabled = autocompletionEnabled;
    if (autocompletionEnabled) {
      _controller.autocompleter.setCustomWords(autocompletionWords);
    } else {
      _controller.autocompleter.setCustomWords(const []);
      _controller.popupController.hide();
    }

    Widget editor = SingleChildScrollView(
        child: fce.CodeField(
      controller: _controller,
      focusNode: _focusNode,
      readOnly: widget.control.disabled,
      textStyle: textStyle,
      gutterStyle: gutterStyle,
    ));

    if (themeData != null) {
      editor = fce.CodeTheme(data: themeData, child: editor);
    }

    return LayoutControl(control: widget.control, child: editor);
  }

  bool _listEquals(List<String>? left, List<String>? right) {
    if (left == null && right == null) {
      return true;
    }
    if (left == null || right == null) {
      return false;
    }
    if (left.length != right.length) {
      return false;
    }
    for (var i = 0; i < left.length; i++) {
      if (left[i] != right[i]) {
        return false;
      }
    }
    return true;
  }
}

class _FletCodeController extends fce.CodeController {
  _FletCodeController({
    super.text,
    super.language,
    super.analyzer,
    super.namedSectionParser,
    super.readOnlySectionNames,
    super.visibleSectionNames,
    super.analysisResult,
    super.patternMap,
    super.readOnly,
    super.params,
    super.modifiers,
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
