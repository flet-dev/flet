import 'package:flutter/widgets.dart';
import '../models/control.dart';
import 'create_control.dart';

class ExpandedControl extends StatelessWidget {
  final Control control;
  final List<Control> children;

  const ExpandedControl(
      {Key? key, required this.control, required this.children})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Expanded build: ${control.id}");
    if (control.childIds.isEmpty) {
      return const SizedBox.shrink();
    } else {
      return Expanded(child: createControl(control.childIds.first));
    }
  }
}
