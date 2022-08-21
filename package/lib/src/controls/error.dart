import 'package:flutter/material.dart';

class ErrorControl extends StatelessWidget {
  final String message;

  const ErrorControl(this.message, {Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Error build");
    return Container(
      padding: const EdgeInsets.all(5),
      decoration: BoxDecoration(
          color: Colors.red, borderRadius: BorderRadius.circular(3)),
      child: Text(message, style: const TextStyle(color: Colors.white)),
    );
  }
}
