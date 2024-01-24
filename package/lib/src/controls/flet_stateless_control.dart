import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_tree_view_model.dart';
import '../models/page_args_model.dart';

abstract class FletStatelessControl extends StatelessWidget {
  const FletStatelessControl({super.key});

  Widget withPageArgs(Widget Function(BuildContext, PageArgsModel) build) {
    return StoreConnector<AppState, PageArgsModel>(
        distinct: true,
        converter: (store) => PageArgsModel.fromStore(store),
        builder: build);
  }

  Widget withControlTree(Control control,
      Widget Function(BuildContext, ControlTreeViewModel) build) {
    return StoreConnector<AppState, ControlTreeViewModel>(
        distinct: true,
        converter: (store) => ControlTreeViewModel.fromStore(store, control),
        builder: build);
  }
}
