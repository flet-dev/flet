import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class ControlViewModel extends Equatable {
  final Control control;
  final List<Control> children;

  const ControlViewModel({required this.control, required this.children});

  static ControlViewModel fromStore(Store<AppState> store, String id) {
    return ControlViewModel(
        control: store.state.controls[id]!,
        children: store.state.controls[id]!.childIds
            .map((childId) => store.state.controls[childId]!)
            .toList());
  }

  @override
  List<Object?> get props => [control, children];
}
