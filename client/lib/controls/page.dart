import '../widgets/screen_size.dart';
import 'package:flutter/material.dart';
import 'create_control.dart';
import '../models/control.dart';

class PageControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;

  const PageControl(
      {Key? key, this.parent, required this.control, required this.children})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Page build: ${control.id}");

    bool disabled = control.attrBool("disabled", false)!;

    var themeMode = ThemeMode.values.firstWhere(
        (element) => element.name == control.attrString("themeMode"),
        orElse: () => ThemeMode.system);

    return MaterialApp(
      themeMode: themeMode,
      home: Scaffold(
        body: Column(
          children: control.childIds
              .map((childId) => createControl(control, childId, disabled))
              .toList()
            ..add(const ScreenSize()),
        ),
      ),
    );
  }
}
