import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class ControlChildrenViewModel extends Equatable {
  final List<Control> children;
  final dynamic dispatch;

  const ControlChildrenViewModel({required this.children, this.dispatch});

  static ControlChildrenViewModel fromStore(Store<AppState> store, String id,
      {dynamic dispatch}) {
    return ControlChildrenViewModel(
        children: store.state.controls[id]!.childIds
            .map((childId) => store.state.controls[childId]!)
            .toList(),
        dispatch: dispatch);
  }

  @override
  List<Object?> get props => [children];
}
