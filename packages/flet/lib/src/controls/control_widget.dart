import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/keys.dart';
import '../widgets/control_inherited_notifier.dart';
import '../widgets/error.dart';

/// Builds the Flutter [Widget] for a [Control].
///
/// Responsibilities:
/// - Resolves a stable Flutter [Key] from the control's `key` property (including
///   registering a scroll [GlobalKey] with the backend).
/// - Delegates widget creation to registered extensions.
/// - Wraps the result in:
///   [ControlInheritedNotifier] (reactivity) and per-control theme overrides.
class ControlWidget extends StatelessWidget {
  final Control control;

  const ControlWidget({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    ControlKey? controlKey = control.getKey("key");
    Key? key;
    if (controlKey is ControlScrollKey) {
      // A scroll key needs to be a GlobalKey so the backend can access state.
      key = GlobalKey();
      FletBackend.of(context).globalKeys[controlKey.toString()] =
          key as GlobalKey;
    } else if (controlKey != null) {
      key = ValueKey(controlKey.value);
    }

    return wrapWithControlInheritedNotifierAndTheme(control, (context) {
      for (var extension in FletBackend.of(context).extensions) {
        final widget = extension.createWidget(key, control);
        if (widget != null) return widget;
      }
      return ErrorControl("Unknown control: ${control.type}");
    });
  }
}
