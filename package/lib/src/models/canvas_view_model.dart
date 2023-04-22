import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';
import 'control_tree_view_model.dart';

class CanvasViewModel extends Equatable {
  final Control control;
  final Control? child;
  final List<ControlTreeViewModel> shapes;
  final dynamic dispatch;

  const CanvasViewModel(
      {required this.control,
      required this.child,
      required this.shapes,
      required this.dispatch});

  static CanvasViewModel fromStore(
      Store<AppState> store, Control control, List<Control> children) {
    return CanvasViewModel(
        control: control,
        child: store.state.controls[control.id]!.childIds
            .map((childId) => store.state.controls[childId])
            .whereNotNull()
            .where((c) => c.name == "content" && c.isVisible)
            .firstOrNull,
        shapes: children
            .where((c) => c.name != "content" && c.isVisible)
            .map((c) => ControlTreeViewModel.fromStore(store, c))
            .toList(),
        dispatch: store.dispatch);
  }

  @override
  List<Object?> get props => [control, shapes, dispatch];
}
