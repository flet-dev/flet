import 'package:flutter/material.dart';

class LoadingPage extends StatelessWidget {
  final bool isLoading;
  final String message;

  const LoadingPage({Key? key, required this.isLoading, required this.message})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    Widget? child;

    var theme = Theme.of(context);

    if (isLoading) {
      List<Widget> children = [
        const SizedBox(
          width: 30,
          height: 30,
          child: CircularProgressIndicator(
            strokeWidth: 3,
          ),
        )
      ];
      if (message != "") {
        children.addAll([
          const SizedBox(height: 8),
          Text(
            message,
            style: Theme.of(context).textTheme.bodySmall,
          )
        ]);
      }
      child = Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: children,
      );
    } else if (message != "") {
      child = Container(
        margin: const EdgeInsets.all(20),
        padding: const EdgeInsets.all(10),
        decoration: BoxDecoration(
            color: theme.colorScheme.errorContainer,
            borderRadius: BorderRadius.circular(8)),
        child: Row(mainAxisSize: MainAxisSize.min, children: [
          Icon(Icons.error_outline,
              color: theme.colorScheme.onErrorContainer, size: 30),
          const SizedBox(width: 8),
          Flexible(
              child: Text(
            message,
            softWrap: true,
            style: Theme.of(context)
                .textTheme
                .bodySmall!
                .copyWith(color: theme.colorScheme.onErrorContainer),
          ))
        ]),
      );
    }

    return Scaffold(
      backgroundColor: Colors.transparent,
      body: Container(
          alignment: Alignment.center,
          color: theme.colorScheme.surface.withOpacity(0.7),
          child: child),
    );
  }
}
