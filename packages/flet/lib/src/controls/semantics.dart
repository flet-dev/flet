import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import 'create_control.dart';

class SemanticsControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const SemanticsControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("Semantics build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    var label = control.attrString("label");
    bool disabled = control.isDisabled || parentDisabled;

    Semantics semantics = Semantics(
        label: label,
        enabled: !disabled,
        expanded: control.attrBool("expanded", false),
        hidden: control.attrBool("hidden", false),
        selected: control.attrBool("selected", false),
        onTap: control.attrBool("onclick", false)!
            ? () {
                backend.triggerControlEvent(control.id, "click", '');
              }
            : null,
        checked: control.attrBool("checked", false),
        button: control.attrBool("button", false),
        slider: control.attrBool("slider", false),
        value: control.attrString("value"),
        increasedValue: control.attrString("increasedValue"),
        decreasedValue: control.attrString("decreasedValue"),
        hint: control.attrString("hint"),
        onTapHint: control.attrString("onTapHint"),
        onLongPressHint: control.attrString("onLongPressHint"),
        container: control.attrBool("container", false)!,
        liveRegion: control.attrBool("liveRegion", false),
        onIncrease: control.attrBool("onIncrease", false)!
            ? () {
                backend.triggerControlEvent(control.id, "increase", '');
              }
            : null,
        onDecrease: control.attrBool("onDecrease", false)!
            ? () {
                backend.triggerControlEvent(control.id, "decrease", '');
              }
            : null,
        onDismiss: control.attrBool("onDismiss", false)!
            ? () {
                backend.triggerControlEvent(control.id, "dismiss", '');
              }
            : null,
        onScrollLeft: control.attrBool("onScrollLeft", false)!
            ? () {
                backend.triggerControlEvent(control.id, "scrollLeft", '');
              }
            : null,
        onScrollRight: control.attrBool("onScrollRight", false)!
            ? () {
                backend.triggerControlEvent(control.id, "scrollRight", '');
              }
            : null,
        onScrollUp: control.attrBool("onScrollUp", false)!
            ? () {
                backend.triggerControlEvent(control.id, "scrollUp", '');
              }
            : null,
        onScrollDown: control.attrBool("onScrollDown", false)!
            ? () {
                backend.triggerControlEvent(control.id, "scrollDown", '');
              }
            : null,
        onCopy: control.attrBool("onCopy", false)!
            ? () {
                backend.triggerControlEvent(control.id, "copy", '');
              }
            : null,
        onCut: control.attrBool("onCut", false)!
            ? () {
                backend.triggerControlEvent(control.id, "cut", '');
              }
            : null,
        onPaste: control.attrBool("onPaste", false)!
            ? () {
                backend.triggerControlEvent(control.id, "paste", '');
              }
            : null,
        onLongPress: control.attrBool("onDismissed", false)!
            ? () {
                backend.triggerControlEvent(control.id, "dismissed", '');
              }
            : null,
        onMoveCursorForwardByCharacter:
            control.attrBool("onMoveCursorForwardByCharacter", false)!
                ? (bool value) {
                    backend.triggerControlEvent(control.id,
                        "move_cursor_forward_by_character", value.toString());
                  }
                : null,
        onMoveCursorBackwardByCharacter:
            control.attrBool("onMoveCursorBackwardByCharacter", false)!
                ? (bool value) {
                    backend.triggerControlEvent(control.id,
                        "move_cursor_backward_by_character", value.toString());
                  }
                : null,
        onDidGainAccessibilityFocus:
            control.attrBool("onDidGainAccessibilityFocus", false)!
                ? () {
                    backend.triggerControlEvent(
                        control.id, "did_gain_accessibility_focus", '');
                  }
                : null,
        onDidLoseAccessibilityFocus:
            control.attrBool("onDidLoseAccessibilityFocus", false)!
                ? () {
                    backend.triggerControlEvent(
                        control.id, "did_lose_accessibility_focus", '');
                  }
                : null,
        obscured: control.attrBool("obscured", false),
        multiline: control.attrBool("multiline", false),
        focused: control.attrBool("focused", false),
        readOnly: control.attrBool("readOnly", false),
        focusable: control.attrBool("focusable", true),
        tooltip: control.attrString("tooltip"),
        toggled: control.attrBool("toggled", false),
        maxValueLength: control.attrInt("maxValueLength"),
        child: contentCtrls.isNotEmpty
            ? createControl(control, contentCtrls.first.id, disabled,
                parentAdaptive: parentAdaptive)
            : null);

    return constrainedControl(context, semantics, parent, control);
  }
}
