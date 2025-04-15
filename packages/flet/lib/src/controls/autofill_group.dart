import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/autofill.dart';
import '../widgets/error.dart';

class AutofillGroupControl extends StatelessWidget {
  final Control control;

  const AutofillGroupControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("AutofillGroup build: ${control.id}");

    var content = control.buildWidget("content");

    if (content == null) {
      return const ErrorControl("AutofillGroup control has no content.");
    }

    return AutofillGroup(
        onDisposeAction: control.getAutofillContextAction(
            "dispose_action", AutofillContextAction.commit)!,
        child: content);
  }
}
