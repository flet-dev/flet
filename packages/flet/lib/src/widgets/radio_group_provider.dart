import 'package:flutter/material.dart';

import '../models/control.dart';

class RadioGroupProvider extends InheritedWidget {
  final Control radioGroupControl;

  const RadioGroupProvider({
    super.key,
    required this.radioGroupControl,
    required super.child,
  });

  static Control? of(BuildContext context) {
    return context
        .dependOnInheritedWidgetOfExactType<RadioGroupProvider>()
        ?.radioGroupControl;
  }

  @override
  bool updateShouldNotify(RadioGroupProvider oldWidget) {
    return oldWidget.radioGroupControl != radioGroupControl;
  }
}
