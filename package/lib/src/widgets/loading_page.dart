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
      child = Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
                color: theme.colorScheme.errorContainer,
                borderRadius: BorderRadius.circular(8)),
            child: Row(children: [
              Icon(Icons.error_outline,
                  color: theme.colorScheme.onErrorContainer, size: 30),
              const SizedBox(width: 8),
              Text(
                message,
                style: Theme.of(context)
                    .textTheme
                    .bodySmall!
                    .copyWith(color: theme.colorScheme.onErrorContainer),
              )
            ]),
          )
        ],
      );
    }

    return Container(
        alignment: Alignment.center,
        color: theme.colorScheme.surface.withOpacity(0.7),
        child: child);
  }
}
