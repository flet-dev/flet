import 'package:flutter/material.dart';

class FletAppContext extends InheritedWidget {
  final ThemeMode? themeMode;

  const FletAppContext(
      {super.key, required this.themeMode, required super.child});

  @override
  bool updateShouldNotify(covariant InheritedWidget oldWidget) {
    return false;
  }

  static FletAppContext? of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<FletAppContext>();
}
