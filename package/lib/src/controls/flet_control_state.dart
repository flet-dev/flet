import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_ancestor_view_model.dart';
import '../models/control_tree_view_model.dart';
import '../models/control_view_model.dart';
import '../models/controls_view_model.dart';
import '../models/page_args_model.dart';
import '../models/page_size_view_model.dart';

abstract class FletControlState<T extends StatefulWidget> extends State<T> {
  Widget withPageArgs(Widget Function(BuildContext, PageArgsModel) build) {
    return StoreConnector<AppState, PageArgsModel>(
        distinct: true,
        converter: (store) => PageArgsModel.fromStore(store),
        builder: build);
  }

  Widget withPageUri(Widget Function(BuildContext, Uri?) build) {
    return StoreConnector<AppState, Uri?>(
        distinct: true,
        converter: (store) => store.state.pageUri,
        builder: build);
  }

  Widget withPageSize(Widget Function(BuildContext, PageSizeViewModel) build) {
    return StoreConnector<AppState, PageSizeViewModel>(
        distinct: true,
        converter: (store) => PageSizeViewModel.fromStore(store),
        builder: build);
  }

  Widget withControl(
      String id, Widget Function(BuildContext, ControlViewModel?) build) {
    return StoreConnector<AppState, ControlViewModel?>(
        distinct: true,
        converter: (store) {
          return ControlViewModel.fromStore(store, id);
        },
        ignoreChange: (state) {
          return state.controls[id] == null;
        },
        builder: build);
  }

  Widget withControlTree(Control control,
      Widget Function(BuildContext, ControlTreeViewModel) build) {
    return StoreConnector<AppState, ControlTreeViewModel>(
        distinct: true,
        converter: (store) => ControlTreeViewModel.fromStore(store, control),
        builder: build);
  }

  Widget withControlAncestor(String id, String ancestorType,
      Widget Function(BuildContext, ControlAncestorViewModel) build) {
    return StoreConnector<AppState, ControlAncestorViewModel>(
        distinct: true,
        converter: (store) =>
            ControlAncestorViewModel.fromStore(store, id, ancestorType),
        ignoreChange: (state) {
          return state.controls[id] == null;
        },
        builder: build);
  }

  Widget withControls(Iterable<String> controlIds,
      Widget Function(BuildContext, ControlsViewModel) build) {
    return StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(store, controlIds),
        ignoreChange: (state) {
          for (var id in controlIds) {
            if (state.controls[id] == null) {
              return true;
            }
          }
          return false;
        },
        builder: build);
  }
}
