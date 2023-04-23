import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class ControlTreeViewModel extends Equatable {
  final Control control;
  final List<ControlTreeViewModel> children;

  const ControlTreeViewModel({required this.control, required this.children});

  static ControlTreeViewModel fromStore(
      Store<AppState> store, Control control) {
    return ControlTreeViewModel(
        control: control,
        children: control.childIds
            .map((childId) => store.state.controls[childId])
            .whereNotNull()
            .where((c) => c.isVisible)
            .map((c) => ControlTreeViewModel.fromStore(store, c))
            .toList());
  }

  @override
  List<Object?> get props => [control, children];
}
