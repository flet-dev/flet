import 'package:flutter/widgets.dart';

import '../models/control.dart';

/// InheritedNotifier for Control.
class ControlInheritedNotifier extends InheritedNotifier<Control> {
  const ControlInheritedNotifier({
    super.key,
    super.notifier,
    required super.child,
  }) : super();

  static Control? of(BuildContext context) {
    return context
        .dependOnInheritedWidgetOfExactType<ControlInheritedNotifier>()
        ?.notifier;
  }

  @override
  bool updateShouldNotify(ControlInheritedNotifier oldWidget) {
    return notifier != oldWidget.notifier;
  }
}
