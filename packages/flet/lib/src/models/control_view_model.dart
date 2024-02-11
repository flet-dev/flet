import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class ControlViewModel extends Equatable {
  final Control control;
  final List<Control> children;
  final dynamic dispatch;

  const ControlViewModel(
      {required this.control, required this.children, required this.dispatch});

  static ControlViewModel? fromStore(Store<AppState> store, String id) {
    var control = store.state.controls[id];
    return control != null
        ? ControlViewModel(
            control: control,
            children: control.childIds
                .map((childId) => store.state.controls[childId])
                .whereNotNull()
                .toList(),
            dispatch: store.dispatch)
        : null;
  }

  @override
  List<Object?> get props => [control, children, dispatch];
}
