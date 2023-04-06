import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'barchart_rod_stack_item_view_model.dart';
import 'control.dart';

class BarChartRodViewModel extends Equatable {
  final Control control;
  final List<BarChartRodStackItemViewModel> rodStackItems;

  const BarChartRodViewModel(
      {required this.control, required this.rodStackItems});

  static BarChartRodViewModel fromStore(
      Store<AppState> store, Control control) {
    return BarChartRodViewModel(
        control: control,
        rodStackItems: store.state.controls[control.id]!.childIds
            .map((childId) => store.state.controls[childId])
            .whereNotNull()
            .where((c) => c.isVisible)
            .map((c) => BarChartRodStackItemViewModel.fromStore(store, c))
            .toList());
  }

  @override
  List<Object?> get props => [control, rodStackItems];
}
