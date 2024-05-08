import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/auto_complete.dart';
import 'create_control.dart';

class AutoCompleteControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const AutoCompleteControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("AutoComplete build: ${control.id}");

    var suggestionsMaxHeight = control.attrDouble("suggestionsMaxHeight", 200)!;
    var suggestions = parseAutoCompleteSuggestions(control, "suggestions");

    var auto = Autocomplete(
      optionsMaxHeight: suggestionsMaxHeight,
      onSelected: (AutoCompleteSuggestion selection) {
        backend.triggerControlEvent(
            control.id,
            "select",
            //suggestions.indexOf(selection).toString()
            json.encode(AutoCompleteSuggestion(
                    key: selection.key, value: selection.value)
                .toJson()));
      },
      // optionsViewBuilder: optionsViewBuilder,
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
    );

    return baseControl(context, auto, parent, control);
  }
}
