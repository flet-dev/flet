import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/auto_complete.dart';
import 'base_controls.dart';

class AutoCompleteControl extends StatelessWidget {
  final Control control;

  const AutoCompleteControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("AutoComplete build: ${control.id}");

    var suggestions =
        parseAutoCompleteSuggestions(control.get("suggestions"), const [])!;

    var autoComplete = Autocomplete(
      optionsMaxHeight: control.getDouble("suggestions_max_height", 200)!,
      onSelected: (AutoCompleteSuggestion selection) {
        control.triggerEvent("select", {
          "selection": selection.toMap(),
          "selection_index": suggestions.indexOf(selection)
        });
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

    return BaseControl(control: control, child: autoComplete);
  }
}
