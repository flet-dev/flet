import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/auto_complete.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class AutoCompleteControl extends StatefulWidget {
  final Control control;

  const AutoCompleteControl({super.key, required this.control});

  @override
  State<AutoCompleteControl> createState() => _AutoCompleteControlState();
}

class _AutoCompleteControlState extends State<AutoCompleteControl> {
  TextEditingController? _controller;
  bool _isSyncingController = false;
  String _value = "";

  @override
  void dispose() {
    _controller?.removeListener(_handleTextChanged);
    super.dispose();
  }

  void _attachController(TextEditingController controller) {
    if (identical(_controller, controller)) return;
    _controller?.removeListener(_handleTextChanged);
    _controller = controller;
    _controller!.addListener(_handleTextChanged);
    _syncController();
  }

  void _syncController() {
    final controller = _controller;
    if (controller == null || controller.text == _value) return;

    _isSyncingController = true;
    controller.value = TextEditingValue(
      text: _value,
      selection: TextSelection.collapsed(offset: _value.length),
    );
    _isSyncingController = false;
  }

  void _handleTextChanged() {
    final controller = _controller;
    if (_isSyncingController || controller == null) return;

    final value = controller.text;
    if (value == _value) return;
    _value = value;

    widget.control.updateProperties({"value": value});
    widget.control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("AutoComplete build: ${widget.control.id}");

    var suggestions = parseAutoCompleteSuggestions(
        widget.control.get("suggestions"), const [])!;

    var controlValue = widget.control.getString("value", "")!;
    if (_value != controlValue) {
      _value = controlValue;
      _syncController();
    }

    var autoComplete = Autocomplete(
      optionsMaxHeight:
          widget.control.getDouble("suggestions_max_height", 200)!,
      onSelected: (AutoCompleteSuggestion selection) {
        final index = suggestions.indexOf(selection);
        widget.control.updateProperties({"_selected_index": index});
        widget.control.triggerEvent(
            "select", {"index": index, "selection": selection.toMap()});
      },
      optionsBuilder: (TextEditingValue textEditingValue) {
        if (textEditingValue.text == '') {
          return const Iterable<AutoCompleteSuggestion>.empty();
        }
        return suggestions.where((AutoCompleteSuggestion suggestion) {
          return suggestion
              .selectionString()
              .toLowerCase()
              .contains(textEditingValue.text.toLowerCase());
        });
      },
      fieldViewBuilder: (BuildContext context,
          TextEditingController textEditingController,
          FocusNode focusNode,
          VoidCallback onFieldSubmitted) {
        _attachController(textEditingController);
        return TextField(
          controller: textEditingController,
          focusNode: focusNode,
          onEditingComplete: onFieldSubmitted,
          onSubmitted: (_) => onFieldSubmitted(),
        );
      },
    );

    return LayoutControl(control: widget.control, child: autoComplete);
  }
}
