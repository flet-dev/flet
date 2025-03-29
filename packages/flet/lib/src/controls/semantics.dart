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

    var contentCtrls = children.where((c) => c.name == "content" && c.visible);
    bool disabled = control.disabled || parentDisabled;

    Semantics semantics = Semantics(
        label: control.getString("label"),
        enabled: !disabled,
        expanded: control.getBool("expanded"),
        hidden: control.getBool("hidden"),
        selected: control.getBool("selected"),
        checked: control.getBool("checked"),
        button: control.getBool("button"),
        slider: control.getBool("slider"),
        value: control.getString("value"),
        textField: control.getBool("textField"),
        image: control.getBool("image"),
        link: control.getBool("link"),
        header: control.getBool("header"),
        increasedValue: control.getString("increasedValue"),
        decreasedValue: control.getString("decreasedValue"),
        hint: control.getString("hint"),
        onTapHint: control.getString("onTapHint"),
        onLongPressHint: control.getString("onLongPressHint"),
        container: control.getBool("container")!,
        liveRegion: control.getBool("liveRegion"),
        obscured: control.getBool("obscured"),
        multiline: control.getBool("multiline"),
        focused: control.getBool("focused"),
        readOnly: control.getBool("readOnly"),
        focusable: control.getBool("focusable"),
        tooltip: control.getString("tooltip"),
        toggled: control.getBool("toggled"),
        maxValueLength: control.getInt("maxValueLength"),
        currentValueLength: control.getInt("currentValueLength"),
        headingLevel: control.getInt("headingLevel"),
        excludeSemantics: control.getBool("excludeSemantics", false)!,
        mixed: control.getBool("mixed"),
        onTap: control.getBool("onclick", false)!
            ? () {
                backend.triggerControlEvent(control.id, "click");
              }
            : null,
        onIncrease: control.getBool("onIncrease", false)!
            ? () {
                backend.triggerControlEvent(control.id, "increase");
              }
            : null,
        onDecrease: control.getBool("onDecrease", false)!
            ? () {
                backend.triggerControlEvent(control.id, "decrease");
              }
            : null,
        onDismiss: control.getBool("onDismiss", false)!
            ? () {
                backend.triggerControlEvent(control.id, "dismiss");
              }
            : null,
        onScrollLeft: control.getBool("onScrollLeft", false)!
            ? () {
                backend.triggerControlEvent(control.id, "scrollLeft");
              }
            : null,
        onScrollRight: control.getBool("onScrollRight", false)!
            ? () {
                backend.triggerControlEvent(control.id, "scrollRight");
              }
            : null,
        onScrollUp: control.getBool("onScrollUp", false)!
            ? () {
                backend.triggerControlEvent(control.id, "scrollUp");
              }
            : null,
        onScrollDown: control.getBool("onScrollDown", false)!
            ? () {
                backend.triggerControlEvent(control.id, "scrollDown");
              }
            : null,
        onCopy: control.getBool("onCopy", false)!
            ? () {
                backend.triggerControlEvent(control.id, "copy");
              }
            : null,
        onCut: control.getBool("onCut", false)!
            ? () {
                backend.triggerControlEvent(control.id, "cut");
              }
            : null,
        onPaste: control.getBool("onPaste", false)!
            ? () {
                backend.triggerControlEvent(control.id, "paste");
              }
            : null,
        onLongPress: control.getBool("onDismiss", false)!
            ? () {
                backend.triggerControlEvent(control.id, "dismiss");
              }
            : null,
        onMoveCursorForwardByCharacter:
            control.getBool("onMoveCursorForwardByCharacter", false)!
                ? (bool value) {
                    backend.triggerControlEvent(control.id,
                        "move_cursor_forward_by_character", value.toString());
                  }
                : null,
        onMoveCursorBackwardByCharacter:
            control.getBool("onMoveCursorBackwardByCharacter", false)!
                ? (bool value) {
                    backend.triggerControlEvent(control.id,
                        "move_cursor_backward_by_character", value.toString());
                  }
                : null,
        onDidGainAccessibilityFocus:
            control.getBool("onDidGainAccessibilityFocus", false)!
                ? () {
                    backend.triggerControlEvent(
                        control.id, "did_gain_accessibility_focus");
                  }
                : null,
        onDidLoseAccessibilityFocus:
            control.getBool("onDidLoseAccessibilityFocus", false)!
                ? () {
                    backend.triggerControlEvent(
                        control.id, "did_lose_accessibility_focus");
                  }
                : null,
        onSetText: control.getBool("onSetText", false)!
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
