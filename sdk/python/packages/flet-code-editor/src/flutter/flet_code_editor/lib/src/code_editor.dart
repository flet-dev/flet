import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_code_editor/flutter_code_editor.dart' as fce;
import 'package:highlight/languages/all.dart';

import 'utils/code_editor.dart';
import 'utils/flet_code_controller.dart';

class CodeEditorControl extends StatefulWidget {
  final Control control;

  const CodeEditorControl({super.key, required this.control});

  @override
  State<CodeEditorControl> createState() => _CodeEditorControlState();
}

class _CodeEditorControlState extends State<CodeEditorControl> {
  late FletCodeController _controller;
  late final FocusNode _focusNode;
  bool _didAutoFocus = false;
  TextSelection? _selection;
  String _value = "";
  String? _languageName;
  Timer? _analyzeDebounce;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
    _controller = _createController();
    _value = _readValue();
    _selection = _controller.selection;
    _controller.addListener(_handleControllerChange);
    widget.control.addInvokeMethodListener(_invokeMethod);
    _scheduleAnalyzeEvent(immediate: true);
  }

  @override
  void dispose() {
    _analyzeDebounce?.cancel();
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
        _controller.foldCommentAtLineZero();
        break;
      case "fold_imports":
        _controller.foldImports();
        break;
      case "fold_at":
        final line = parseInt(args["line_number"]);
        if (line != null) {
          _controller.foldAt(line);
        }
        break;
      default:
        throw Exception("Unknown CodeEditor method: $name");
    }
  }

  void _onFocusChange() {
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  FletCodeController _createController() {
    _languageName = widget.control.get("language", "")!;
    return FletCodeController(
      text: _initialValueFromControl(),
      language: allLanguages[_languageName!.toLowerCase()],
      externalAnalysisEnabled: _usesExternalAnalysis(),
    );
  }

  String _initialValueFromControl() {
    return widget.control.getString("value") ?? "";
  }

  List<String>? _stringList(dynamic value) {
    if (value is List) {
      return value.map((e) => e.toString()).toList();
    }
    return null;
  }

  String _readValue() => _controller.fullText;

  void _setValue(String value) {
    _controller.fullText = value;
  }

  bool _usesExternalAnalysis() {
    return widget.control.getBool("on_analyze", false)!;
  }

  List<fce.Issue> _readIssues() {
    final rawIssues = widget.control.get("issues");
    if (rawIssues is! List) {
      return const [];
    }

    return rawIssues
        .whereType<Map>()
        .map(_parseIssue)
        .whereType<fce.Issue>()
        .toList(growable: false);
  }

  fce.Issue? _parseIssue(Map<dynamic, dynamic> rawIssue) {
    final line = parseInt(rawIssue["line"]);
    final message = rawIssue["message"]?.toString();

    if (line == null || message == null || message.isEmpty) {
      return null;
    }

    return fce.Issue(
      line: line,
      message: message,
      type: _parseIssueType(rawIssue["type"]),
      suggestion: rawIssue["suggestion"]?.toString(),
      url: rawIssue["url"]?.toString(),
    );
  }

  fce.IssueType _parseIssueType(dynamic rawType) {
    switch (rawType?.toString()) {
      case "info":
        return fce.IssueType.info;
      case "warning":
        return fce.IssueType.warning;
      default:
        return fce.IssueType.error;
    }
  }

  void _scheduleAnalyzeEvent({bool immediate = false}) {
    if (!_usesExternalAnalysis()) {
      return;
    }

    // ISSUE-6312: Delegate code analysis to Python when on_analyze is wired.
    _analyzeDebounce?.cancel();
    if (!immediate) {
      _controller.setIssues(const []);
    }

    void triggerAnalyze() {
      if (!mounted || !_usesExternalAnalysis()) {
        return;
      }

      widget.control.triggerEvent("analyze", {
        "value": _readValue(),
        "language": _languageName,
        if (_controller.selection.isValid)
          "selection": _controller.selection.toMap(),
      });
    }

    if (immediate) {
      WidgetsBinding.instance.addPostFrameCallback((_) => triggerAnalyze());
      return;
    }

    _analyzeDebounce = Timer(
      const Duration(milliseconds: 500),
      triggerAnalyze,
    );
  }

  void _handleControllerChange() {
    final value = _readValue();
    final selection = _controller.selection;
    final selectionChanged = selection != _selection;
    final valueChanged = value != _value;

    if (!valueChanged && !selectionChanged) {
      return;
    }

    _value = value;
    _selection = selection;

    final updates = <String, dynamic>{};

    if (valueChanged) {
      updates["value"] = value;
    }

    if (selectionChanged) {
      if (selection.isValid) {
        updates["selection"] = selection.toMap();
      } else {
        updates["selection"] = null;
      }
    }

    if (updates.isNotEmpty) {
      widget.control.updateProperties(updates);
    }

    if (valueChanged && widget.control.getBool("on_change", false)!) {
      widget.control.triggerEvent("change", value);
    }

    if (valueChanged) {
      _scheduleAnalyzeEvent();
    }

    if (selectionChanged && selection.isValid) {
      final visibleText = _controller.text;
      widget.control.triggerEvent("selection_change", {
        "selected_text": visibleText.substring(selection.start, selection.end),
        "selection": selection.toMap(),
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CodeEditor build: ${widget.control.id}");

    final languageName = widget.control.get("language", "")!;
    final usesExternalAnalysis = _usesExternalAnalysis();
    if (languageName != _languageName ||
        usesExternalAnalysis != _controller.externalAnalysisEnabled) {
      final previousSelection = _controller.selection;
      _controller.removeListener(_handleControllerChange);
      _controller.dispose();
      _controller = _createController();
      _value = _readValue();
      _controller.addListener(_handleControllerChange);
      if (previousSelection.isValid) {
        _controller.selection = previousSelection;
      }
      _scheduleAnalyzeEvent(immediate: true);
    }

    final value = widget.control.getString("value");
    final controllerValue = _readValue();
    if (value != null && value != controllerValue) {
      _setValue(value);
      _value = value;
    }

    final explicitSelection = widget.control.getTextSelection(
      "selection",
      minOffset: 0,
      maxOffset: _controller.text.length,
    );
    if (explicitSelection != null &&
        explicitSelection != _controller.selection) {
      _controller.selection = explicitSelection;
    }

    _controller.setIssues(_readIssues());

    final autofocus = widget.control.getBool("autofocus", false)!;
    if (!_didAutoFocus && autofocus) {
      _didAutoFocus = true;
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) {
          FocusScope.of(context).autofocus(_focusNode);
        }
      });
    }

    final themeData = parseCodeThemeData(widget.control, context);
    final gutterStyle = parseGutterStyle(widget.control, context);
    final autocompleteEnabled = widget.control.getBool("autocomplete", false)!;
    final autocompleteWords =
        _stringList(widget.control.get("autocomplete_words")) ?? const [];
    _controller.autocompletionEnabled = autocompleteEnabled;
    if (autocompleteEnabled) {
      _controller.autocompleter.setCustomWords(autocompleteWords);
    } else {
      _controller.autocompleter.setCustomWords(const []);
      _controller.popupController.hide();
    }

    Widget editor = SingleChildScrollView(
        child: fce.CodeField(
      controller: _controller,
      focusNode: _focusNode,
      readOnly: widget.control.getBool("read_only", false)!,
      textStyle: widget.control.getTextStyle("text_style", Theme.of(context)),
      gutterStyle: gutterStyle,
      padding: widget.control.getEdgeInsets("padding", EdgeInsets.zero)!,
      enabled: !widget.control.disabled,
    ));

    if (themeData != null) {
      editor = fce.CodeTheme(data: themeData, child: editor);
    }

    return LayoutControl(control: widget.control, child: editor);
  }
}
