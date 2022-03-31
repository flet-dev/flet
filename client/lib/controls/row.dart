import 'package:flutter/widgets.dart';
import '../models/control.dart';
import 'create_control.dart';

class RowControl extends StatelessWidget {
  final Control control;
  final List<Control> children;

  const RowControl({Key? key, required this.control, required this.children})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Row build: ${control.id}");
    return Row(
      mainAxisAlignment: MainAxisAlignment.start,
      children:
          control.childIds.map((childId) => createControl(childId)).toList(),
    );
  }
}
