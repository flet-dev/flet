
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';

class KeyboardListenerControl extends StatefulWidget {
  final Control control;

  KeyboardListenerControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<KeyboardListenerControl> createState() =>
      _KeyboardListenerControlState();
}

class _KeyboardListenerControlState extends State<KeyboardListenerControl> {
  final FocusNode _focusNode = FocusNode();
  bool _escapeDownSent = false;
  DateTime? _lastSynthesizedEscapeUpAt;

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    _focusNode.dispose();
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("KeyboardListener.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown KeyboardListener method: $name");
    }
  }

  void _triggerKeyEvent(String eventName, KeyEvent keyEvent) {
    if (keyEvent.logicalKey == LogicalKeyboardKey.escape) {
      _escapeDownSent = eventName == "key_down";
    }
    widget.control
        .triggerEvent(eventName, {"key": keyEvent.logicalKey.keyLabel});
  }

  void _triggerEscapeKeyUp() {
    if (!_escapeDownSent) {
      return;
    }
    _escapeDownSent = false;
    widget.control.triggerEvent("key_up", {"key": "Escape"});
  }

  KeyEventResult _handleEscapeLoop(KeyEvent keyEvent) {
    final isEscape = keyEvent.logicalKey == LogicalKeyboardKey.escape;
    final isPhysicalEscape =
        isEscape && keyEvent.physicalKey == PhysicalKeyboardKey.escape;
    final isPeriodEscape =
        isEscape && keyEvent.physicalKey == PhysicalKeyboardKey.period;
    final isMetaUp = keyEvent is KeyUpEvent &&
        (keyEvent.physicalKey == PhysicalKeyboardKey.metaLeft ||
            keyEvent.physicalKey == PhysicalKeyboardKey.metaRight ||
            keyEvent.logicalKey == LogicalKeyboardKey.meta ||
            keyEvent.logicalKey == LogicalKeyboardKey.metaLeft ||
            keyEvent.logicalKey == LogicalKeyboardKey.metaRight);

    if (keyEvent is KeyDownEvent &&
        isPeriodEscape &&
        HardwareKeyboard.instance.isMetaPressed) {
      _triggerKeyEvent("key_down", keyEvent);
      return KeyEventResult.handled;
    }

    if (keyEvent is KeyUpEvent && isPeriodEscape) {
      _triggerEscapeKeyUp();
      return KeyEventResult.handled;
    }

    if (_escapeDownSent && isMetaUp) {
      _triggerEscapeKeyUp();
    }

    if (keyEvent is KeyUpEvent && isPhysicalEscape) {
      _lastSynthesizedEscapeUpAt = DateTime.now();
      if (keyEvent.synthesized) {
        _triggerEscapeKeyUp();
        return KeyEventResult.handled;
      }
    }

    if (keyEvent is KeyDownEvent && isPhysicalEscape) {
      final lastUpAt = _lastSynthesizedEscapeUpAt;
      if (lastUpAt != null &&
          DateTime.now().difference(lastUpAt) <
              const Duration(milliseconds: 300)) {
        return KeyEventResult.handled;
      }
    }

    if (!isEscape) {
      _lastSynthesizedEscapeUpAt = null;
    }

    return KeyEventResult.ignored;
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("KeyboardListener build: ${widget.control.id}");

    var content = widget.control.buildWidget("content");

    if (content == null) {
      return const ErrorControl("KeyboardListener control has no content.");
    }

    return Focus(
      focusNode: _focusNode,
      autofocus: widget.control.getBool("autofocus", false)!,
      includeSemantics: widget.control.getBool("include_semantics", true)!,
      onKeyEvent: (FocusNode node, KeyEvent keyEvent) {
        final result = _handleEscapeLoop(keyEvent);
        if (result == KeyEventResult.handled) {
          return result;
        }
        if (keyEvent is KeyDownEvent) {
          _triggerKeyEvent("key_down", keyEvent);
        } else if (keyEvent is KeyUpEvent) {
          _triggerKeyEvent("key_up", keyEvent);
        } else if (keyEvent is KeyRepeatEvent) {
          _triggerKeyEvent("key_repeat", keyEvent);
        }
        return KeyEventResult.ignored;
      },
      child: content,
    );
  }
}

