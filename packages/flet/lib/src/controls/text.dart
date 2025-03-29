import 'package:flutter/widgets.dart';

import '../models/control.dart';

class TextControl extends StatelessWidget {
  final Control control;
  const TextControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Text.build: ${control.id}");

    String text = control.get<String>("value", "")!;
    return Text(text);
  }
}
