import 'package:flutter/material.dart';

class FletAppContext extends InheritedWidget {
  final ThemeMode? themeMode;

  const FletAppContext(
      {super.key, required this.themeMode, required super.child});

  @override
  bool updateShouldNotify(covariant FletAppContext oldWidget) {
    return themeMode != oldWidget.themeMode;
  }

  static FletAppContext? of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<FletAppContext>();
}
