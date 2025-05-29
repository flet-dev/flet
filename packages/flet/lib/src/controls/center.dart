import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

class CenterControl extends StatelessWidget {
  final Control control;

  const CenterControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Center.build: ${control.id}");
    return Center(child: control.buildWidget("content"));
  }
}
