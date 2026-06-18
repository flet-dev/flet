import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class SemanticsControl extends StatelessWidget {
  final Control control;

  const SemanticsControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Semantics build: ${control.id}");
    final content = control.buildWidget("content");
    Semantics semantics = Semantics(
      child: content ??
          const ErrorControl("Semantics.content must be provided and visible"),
      label: control.getString("label"),
      enabled: !control.disabled,
      expanded: control.getBool("expanded"),
      hidden: control.getBool("hidden"),
      selected: control.getBool("selected"),
      checked: control.getBool("checked"),
      button: control.getBool("button"),
      slider: control.getBool("slider"),
      value: control.getString("value"),
      textField: control.getBool("text_field"),
      image: control.getBool("image"),
      link: control.getBool("link"),
      header: control.getBool("header"),
      increasedValue: control.getString("increased_value"),
      decreasedValue: control.getString("decreased_value"),
      hint: control.getString("hint"),
      onTapHint: control.getString("on_tap_hint"),
      onLongPressHint: control.getString("on_long_press_hint"),
      container: control.getBool("container", false)!,
      liveRegion: control.getBool("live_region"),
      obscured: control.getBool("obscured"),
      multiline: control.getBool("multiline"),
      focused: control.getBool("focused"),
      readOnly: control.getBool("read_only"),
      focusable: control.getBool("focusable"),
      tooltip: control.getString("tooltip"),
      toggled: control.getBool("toggled"),
      maxValueLength: control.getInt("max_value_length"),
      currentValueLength: control.getInt("current_value_length"),
      headingLevel: control.getInt("heading_level"),
      excludeSemantics: control.getBool("exclude_semantics", false)!,
      mixed: control.getBool("mixed"),
      onTap: control.hasEventHandler("click")
          ? () => control.triggerEvent("click")
          : null,
      onIncrease: control.hasEventHandler("increase")
          ? () => control.triggerEvent("increase")
          : null,
      onDecrease: control.hasEventHandler("decrease")
          ? () => control.triggerEvent("decrease")
          : null,
      onDismiss: control.hasEventHandler("dismiss")
          ? () => control.triggerEvent("dismiss")
          : null,
      onScrollLeft: control.hasEventHandler("scroll_left")
          ? () => control.triggerEvent("scroll_left")
          : null,
      onScrollRight: control.hasEventHandler("scroll_right")
          ? () => control.triggerEvent("scroll_right")
          : null,
      onScrollUp: control.hasEventHandler("scroll_up")
          ? () => control.triggerEvent("scroll_up")
          : null,
      onScrollDown: control.hasEventHandler("scroll_down")
          ? () => control.triggerEvent("scroll_down")
          : null,
      onCopy: control.hasEventHandler("copy")
          ? () => control.triggerEvent("copy")
          : null,
      onCut: control.hasEventHandler("cut")
          ? () => control.triggerEvent("cut")
          : null,
      onPaste: control.hasEventHandler("paste")
          ? () => control.triggerEvent("paste")
          : null,
      onLongPress: control.hasEventHandler("long_press")
          ? () => control.triggerEvent("long_press")
          : null,
      onMoveCursorForwardByCharacter: control.getBool(
              "on_move_cursor_forward_by_character", false)!
          ? (bool value) =>
              control.triggerEvent("move_cursor_forward_by_character", value)
          : null,
      onMoveCursorBackwardByCharacter: control.getBool(
              "on_move_cursor_backward_by_character", false)!
          ? (bool value) =>
              control.triggerEvent("move_cursor_backward_by_character", value)
          : null,
      onDidGainAccessibilityFocus:
          control.hasEventHandler("did_gain_accessibility_focus")
              ? () => control.triggerEvent("did_gain_accessibility_focus")
              : null,
      onDidLoseAccessibilityFocus:
          control.hasEventHandler("did_lose_accessibility_focus")
              ? () => control.triggerEvent("did_lose_accessibility_focus")
              : null,
      onSetText: control.hasEventHandler("set_text")
          ? (String text) => control.triggerEvent("set_text", text)
          : null,
    );

    return LayoutControl(control: control, child: semantics);
  }
}
