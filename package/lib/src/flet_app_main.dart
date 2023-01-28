import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:flutter/gestures.dart';

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
                body: Container(
                    padding: const EdgeInsets.all(30),
                    alignment: Alignment.center,
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [const Icon(Icons.error, color: Colors.redAccent, size: 30), const SizedBox(height: 8), Flexible(child: Text(viewModel.error, textAlign: TextAlign.center, style: const TextStyle(color: Colors.red)))],
                    )),
              ),
              scrollBehavior: DragScrollBehavior(),
            );
          } else {
            return createControl(null, "page", false);
          }
        },
      ),
    );
  }
}

class DragScrollBehavior extends MaterialScrollBehavior {
  @override
  Set<PointerDeviceKind> get dragDevices => {
        PointerDeviceKind.touch,
        PointerDeviceKind.mouse,
        PointerDeviceKind.stylus,
        PointerDeviceKind.unknown,
      };
}
