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
  TextSelection? _selection;
  String _text = "";
  String? _fullText;
  String? _languageName;

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

  FletCodeController _createController() {
    _languageName = widget.control.get("language", "")!;
    return FletCodeController(
      text: _initialTextFromControl(),
      language: allLanguages[_languageName!.toLowerCase()],
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

  List<String>? _stringList(dynamic value) {
    if (value is List) {
      return value.map((e) => e.toString()).toList();
    }
    return null;
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

    if (selectionChanged && selection.isValid) {
      widget.control.triggerEvent("selection_change", {
        "selected_text": text.substring(selection.start, selection.end),
        "selection": selection.toMap(),
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CodeEditor build: ${widget.control.id}");

    final languageName = widget.control.get("language", "")!;
    if (languageName != _languageName) {
      final previousSelection = _controller.selection;
      _controller.removeListener(_handleControllerChange);
      _controller.dispose();
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

    final themeData = parseCodeThemeData(widget.control, context);
    final gutterStyle = parseGutterStyle(widget.control, context);
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
      readOnly: widget.control.getBool("read_only", false)!,
      textStyle:
          parseTextStyle(widget.control.get("text_style"), Theme.of(context)),
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
