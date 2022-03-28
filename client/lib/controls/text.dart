import 'package:flutter/widgets.dart';

import '../models/control.dart';

class TextControl extends StatelessWidget {
  final Control control;

  const TextControl({Key? key, required this.control}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Text build: ${control.id}");
    return Text(control.attrs["value"] ?? "");
  }
}
