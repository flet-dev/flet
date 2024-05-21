import 'package:flet/src/utils/autofill.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class AutofillGroupControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const AutofillGroupControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("AutofillGroup build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    if (contentCtrls.isEmpty) {
      return const ErrorControl("AutofillGroup control has no content.");
    }

    return AutofillGroup(
        onDisposeAction: parseAutofillContextAction(
            control.attrString("disposeAction"), AutofillContextAction.commit)!,
        child: createControl(control, contentCtrls.first.id, disabled,
            parentAdaptive: parentAdaptive));
  }
}
