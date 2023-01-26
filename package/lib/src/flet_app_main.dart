import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import 'controls/create_control.dart';
import 'flet_app_services.dart';
import 'models/app_state.dart';
import 'models/page_view_model.dart';

class FletAppMain extends StatelessWidget {
  final String title;

  const FletAppMain({
    Key? key,
    required this.title,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return StoreProvider<AppState>(
      store: FletAppServices.of(context).store,
      child: StoreConnector<AppState, PageViewModel>(
        distinct: true,
        converter: (store) => PageViewModel.fromStore(store),
        builder: (context, viewModel) {
          if (viewModel.error != "" && !viewModel.isLoading) {
            return MaterialApp(
                title: title,
                home: Scaffold(
                  body: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.error_outline,
                          color: Colors.red, size: 25),
                      Text(viewModel.error,
                          style: const TextStyle(color: Colors.red))
                    ],
                  ),
                ));
          } else {
            return createControl(null, "page", false);
          }
        },
      ),
    );
  }
}
