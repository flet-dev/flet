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

  static ControlViewModel fromStore(Store<AppState> store, String id) {
    return ControlViewModel(
        control: store.state.controls[id]!,
        children: store.state.controls[id]!.childIds
            .map((childId) => store.state.controls[childId]!)
            .toList(),
        dispatch: store.dispatch);
  }

  @override
  List<Object?> get props => [control, children, dispatch];
}
