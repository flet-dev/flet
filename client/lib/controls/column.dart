import 'package:flutter/widgets.dart';
import '../models/control.dart';
import 'create_control.dart';

class ColumnControl extends StatelessWidget {
  final Control control;
  final List<Control> children;

  const ColumnControl({Key? key, required this.control, required this.children})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Column build: ${control.id}");
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children:
          control.childIds.map((childId) => createControl(childId)).toList(),
    );
  }
}
