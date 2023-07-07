import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control_view_model.dart';

class ControlsViewModel extends Equatable {
  final List<ControlViewModel> controlViews;

  const ControlsViewModel({required this.controlViews});

  static ControlsViewModel fromStore(
      Store<AppState> store, Iterable<String> ids) {
    return ControlsViewModel(
        controlViews: ids
            .map((id) => ControlViewModel.fromStore(store, id))
            .whereNotNull()
            .toList());
  }

  @override
  List<Object?> get props => [controlViews];
}
