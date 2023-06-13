import 'package:flutter/material.dart';

class FletAppContext extends InheritedWidget {
  final ThemeMode? themeMode;

  const FletAppContext(
      {Key? key, required this.themeMode, required Widget child})
      : super(key: key, child: child);

  @override
  bool updateShouldNotify(covariant InheritedWidget oldWidget) {
    return false;
  }

  static FletAppContext? of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<FletAppContext>();
}
