import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class CustomPaintDrawShapeViewModel extends Equatable {
  final Control control;
  final List<CustomPaintDrawShapeViewModel> shapes;

  const CustomPaintDrawShapeViewModel(
      {required this.control, required this.shapes});

  static CustomPaintDrawShapeViewModel fromStore(
      Store<AppState> store, Control control) {
    return CustomPaintDrawShapeViewModel(
        control: control,
        shapes: store.state.controls[control.id]!.childIds
            .map((childId) => store.state.controls[childId])
            .whereNotNull()
            .where((c) => c.isVisible)
            .map((c) => CustomPaintDrawShapeViewModel.fromStore(store, c))
            .toList());
  }

  @override
  List<Object?> get props => [control, shapes];
}
