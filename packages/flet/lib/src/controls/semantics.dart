import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class SemanticsControl extends StatelessWidget {
  final Control control;

  const SemanticsControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Semantics build: ${control.id}");
    Semantics semantics = Semantics(
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
      container: control.getBool("container")!,
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
      onTap: control.getBool("on_click", false)!
          ? () => control.triggerEvent("click")
          : null,
      onIncrease: control.getBool("on_increase", false)!
          ? () => control.triggerEvent("increase")
          : null,
      onDecrease: control.getBool("on_decrease", false)!
          ? () => control.triggerEvent("decrease")
          : null,
      onDismiss: control.getBool("on_dismiss", false)!
          ? () => control.triggerEvent("dismiss")
          : null,
      onScrollLeft: control.getBool("on_scroll_left", false)!
          ? () => control.triggerEvent("scroll_left")
          : null,
      onScrollRight: control.getBool("on_scroll_right", false)!
          ? () => control.triggerEvent("scroll_right")
          : null,
      onScrollUp: control.getBool("on_scroll_up", false)!
          ? () => control.triggerEvent("scroll_up")
          : null,
      onScrollDown: control.getBool("on_scroll_down", false)!
          ? () => control.triggerEvent("scroll_down")
          : null,
      onCopy: control.getBool("on_copy", false)!
          ? () => control.triggerEvent("copy")
          : null,
      onCut: control.getBool("on_cut", false)!
          ? () => control.triggerEvent("cut")
          : null,
      onPaste: control.getBool("on_paste", false)!
          ? () => control.triggerEvent("paste")
          : null,
      onLongPress: control.getBool("on_dismiss", false)!
          ? () => control.triggerEvent("dismiss")
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
          control.getBool("on_did_gain_accessibility_focus", false)!
              ? () => control.triggerEvent("did_gain_accessibility_focus")
              : null,
      onDidLoseAccessibilityFocus:
          control.getBool("on_did_lose_accessibility_focus", false)!
              ? () => control.triggerEvent("did_lose_accessibility_focus")
              : null,
      onSetText: control.getBool("on_set_text", false)!
          ? (String text) => control.triggerEvent("set_text", text)
          : null,
    );

    return LayoutControl(control: control, child: semantics);
  }
}
