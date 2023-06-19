import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class ControlChildrenViewModel extends Equatable {
  final List<Control> children;

  const ControlChildrenViewModel({required this.children});

  static ControlChildrenViewModel fromStore(Store<AppState> store, String id,
      {dynamic dispatch}) {
    return ControlChildrenViewModel(
        children: store.state.controls[id] != null
            ? store.state.controls[id]!.childIds
                .map((childId) => store.state.controls[childId]!)
                .toList()
            : []);
  }

  @override
  List<Object?> get props => [children];
}
