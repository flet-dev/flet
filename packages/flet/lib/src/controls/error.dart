import 'package:flutter/material.dart';

class ErrorControl extends StatelessWidget {
  final String message;
  final String? description;

  const ErrorControl(this.message, {super.key, this.description});

  @override
  Widget build(BuildContext context) {
    debugPrint("ErrorControl build");
    List<Widget> lines = [
      Text(message, style: const TextStyle(color: Colors.white, fontSize: 12))
    ];
    if (description != null) {
      lines.addAll([
        const SizedBox(height: 5),
        Text(description!,
            style: const TextStyle(color: Colors.white70, fontSize: 11))
      ]);
    }
    return SelectionArea(
        child: Container(
      padding: const EdgeInsets.all(5),
      decoration: BoxDecoration(
          color: Colors.red, borderRadius: BorderRadius.circular(3)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: lines,
      ),
    ));
  }
}
