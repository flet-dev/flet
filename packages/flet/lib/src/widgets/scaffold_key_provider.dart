import 'package:flutter/material.dart';

class ScaffoldKeyProvider extends InheritedWidget {
  final GlobalKey<ScaffoldState> scaffoldKey;

  const ScaffoldKeyProvider({
    super.key,
    required this.scaffoldKey,
    required super.child,
  });

  static GlobalKey<ScaffoldState>? of(BuildContext context) {
    return context
        .dependOnInheritedWidgetOfExactType<ScaffoldKeyProvider>()
        ?.scaffoldKey;
  }

  @override
  bool updateShouldNotify(ScaffoldKeyProvider oldWidget) {
    return oldWidget.scaffoldKey != scaffoldKey;
  }
}
