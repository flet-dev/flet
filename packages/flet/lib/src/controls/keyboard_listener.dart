import 'package:flutter/widgets.dart';
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

  @override
  Widget build(BuildContext context) {
    debugPrint("KeyboardListener build: ${widget.control.id}");

    var content = widget.control.buildWidget("content");

    if (content == null) {
      return const ErrorControl("KeyboardListener control has no content.");
    }

    return KeyboardListener(
      focusNode: _focusNode,
      autofocus: widget.control.getBool("autofocus", false)!,
      includeSemantics: widget.control.getBool("include_semantics", true)!,
      onKeyEvent: (keyEvent) {
        final name = switch (keyEvent) {
          KeyDownEvent() => "key_down",
          KeyUpEvent() => "key_up",
          KeyRepeatEvent() => "key_repeat",
          _ => null,
        };
        if (name != null) {
          widget.control.triggerEvent(name, {
            "key": keyEvent.logicalKey.keyLabel,
            "physical_key": keyEvent.physicalKey.usbHidUsage,
          });
        }
      },
      child: content,
    );
  }
}
