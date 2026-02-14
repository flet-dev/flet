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
      text: _initialValueFromControl(),
      language: allLanguages[_languageName!.toLowerCase()],
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
    if (languageName != _languageName) {
      final previousSelection = _controller.selection;
      _controller.removeListener(_handleControllerChange);
      _controller.dispose();
      _controller = _createController();
      _value = _readValue();
      _controller.addListener(_handleControllerChange);
      if (previousSelection.isValid) {
        _controller.selection = previousSelection;
      }
    }

    final value = widget.control.getString("value");
    final controllerValue = _readValue();
    if (value != null && value != controllerValue) {
      _setValue(value);
      _value = value;
    }

    final explicitSelection = parseTextSelection(
      widget.control.get("selection"),
      minOffset: 0,
      maxOffset: _controller.text.length,
    );
    if (explicitSelection != null && explicitSelection != _controller.selection) {
      _controller.selection = explicitSelection;
    }

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
