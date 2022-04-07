import '../widgets/screen_size.dart';
import 'package:flutter/material.dart';
import 'create_control.dart';
import '../models/control.dart';

class PageControl extends StatelessWidget {
  final Control control;
  final List<Control> children;

  const PageControl({Key? key, required this.control, required this.children})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Page build: ${control.id}");

    return MaterialApp(
      home: Scaffold(
        body: Column(
          children:
              control.childIds.map((childId) => createControl(childId)).toList()
                ..add(const ScreenSize()),
        ),
      ),
    );
  }
}
