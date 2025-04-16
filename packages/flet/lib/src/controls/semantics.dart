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
    bool disabled = control.isDisabled || parentDisabled;

    Semantics semantics = Semantics(
        label: control.attrString("label"),
        enabled: !disabled,
        expanded: control.attrBool("expanded"),
        hidden: control.attrBool("hidden"),
        selected: control.attrBool("selected"),
        checked: control.attrBool("checked"),
        button: control.attrBool("button"),
        slider: control.attrBool("slider"),
        value: control.attrString("value"),
        textField: control.attrBool("textField"),
        image: control.attrBool("image"),
        link: control.attrBool("link"),
        header: control.attrBool("header"),
        increasedValue: control.attrString("increasedValue"),
        decreasedValue: control.attrString("decreasedValue"),
        hint: control.attrString("hint"),
        onTapHint: control.attrString("onTapHint"),
        onLongPressHint: control.attrString("onLongPressHint"),
        container: control.attrBool("container")!,
        liveRegion: control.attrBool("liveRegion"),
        obscured: control.attrBool("obscured"),
        multiline: control.attrBool("multiline"),
        focused: control.attrBool("focused"),
        readOnly: control.attrBool("readOnly"),
        focusable: control.attrBool("focusable"),
        tooltip: control.attrString("tooltip"),
        toggled: control.attrBool("toggled"),
        maxValueLength: control.attrInt("maxValueLength"),
        currentValueLength: control.attrInt("currentValueLength"),
        headingLevel: control.attrInt("headingLevel"),
        excludeSemantics: control.attrBool("excludeSemantics", false)!,
        mixed: control.attrBool("mixed"),
        onTap: control.attrBool("onclick", false)!
            ? () {
                backend.triggerControlEvent(control.id, "click");
              }
            : null,
        onIncrease: control.attrBool("onIncrease", false)!
            ? () {
                backend.triggerControlEvent(control.id, "increase");
              }
            : null,
        onDecrease: control.attrBool("onDecrease", false)!
            ? () {
                backend.triggerControlEvent(control.id, "decrease");
              }
            : null,
        onDismiss: control.attrBool("onDismiss", false)!
            ? () {
                backend.triggerControlEvent(control.id, "dismiss");
              }
            : null,
        onScrollLeft: control.attrBool("onScrollLeft", false)!
            ? () {
                backend.triggerControlEvent(control.id, "scrollLeft");
              }
            : null,
        onScrollRight: control.attrBool("onScrollRight", false)!
            ? () {
                backend.triggerControlEvent(control.id, "scrollRight");
              }
            : null,
        onScrollUp: control.attrBool("onScrollUp", false)!
            ? () {
                backend.triggerControlEvent(control.id, "scrollUp");
              }
            : null,
        onScrollDown: control.attrBool("onScrollDown", false)!
            ? () {
                backend.triggerControlEvent(control.id, "scrollDown");
              }
            : null,
        onCopy: control.attrBool("onCopy", false)!
            ? () {
                backend.triggerControlEvent(control.id, "copy");
              }
            : null,
        onCut: control.attrBool("onCut", false)!
            ? () {
                backend.triggerControlEvent(control.id, "cut");
              }
            : null,
        onPaste: control.attrBool("onPaste", false)!
            ? () {
                backend.triggerControlEvent(control.id, "paste");
              }
            : null,
        onLongPress: control.attrBool("onDismiss", false)!
            ? () {
                backend.triggerControlEvent(control.id, "dismiss");
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
                        control.id, "did_gain_accessibility_focus");
                  }
                : null,
        onDidLoseAccessibilityFocus:
            control.attrBool("onDidLoseAccessibilityFocus", false)!
                ? () {
                    backend.triggerControlEvent(
                        control.id, "did_lose_accessibility_focus");
                  }
                : null,
        onSetText: control.attrBool("onSetText", false)!
            ? (String text) {
                backend.triggerControlEvent(control.id, "set_text", text);
              }
            : null,
        child: contentCtrls.isNotEmpty
            ? createControl(control, contentCtrls.first.id, disabled,
                parentAdaptive: parentAdaptive)
            : null);

    return constrainedControl(context, semantics, parent, control);
  }
}
