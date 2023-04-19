import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class CanvasShapeViewModel extends Equatable {
  final Control control;
  final List<CanvasShapeViewModel> shapes;

  const CanvasShapeViewModel({required this.control, required this.shapes});

  static CanvasShapeViewModel fromStore(
      Store<AppState> store, Control control) {
    return CanvasShapeViewModel(
        control: control,
        shapes: store.state.controls[control.id]!.childIds
            .map((childId) => store.state.controls[childId])
            .whereNotNull()
            .where((c) => c.isVisible)
            .map((c) => CanvasShapeViewModel.fromStore(store, c))
            .toList());
  }

  @override
  List<Object?> get props => [control, shapes];
}
