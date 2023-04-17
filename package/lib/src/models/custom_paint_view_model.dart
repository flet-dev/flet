import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';
import 'custom_paint_draw_shape_view_model.dart';

class CustomPaintViewModel extends Equatable {
  final Control control;
  final List<CustomPaintDrawShapeViewModel> shapes;
  final dynamic dispatch;

  const CustomPaintViewModel(
      {required this.control, required this.shapes, required this.dispatch});

  static CustomPaintViewModel fromStore(
      Store<AppState> store, Control control, List<Control> children) {
    return CustomPaintViewModel(
        control: control,
        shapes: children
            .where((c) => c.isVisible)
            .map((c) => CustomPaintDrawShapeViewModel.fromStore(store, c))
            .toList(),
        dispatch: store.dispatch);
  }

  @override
  List<Object?> get props => [control, shapes, dispatch];
}
