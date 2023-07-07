import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'barchart_rod_view_model.dart';
import 'control.dart';

class BarChartGroupViewModel extends Equatable {
  final Control control;
  final List<BarChartRodViewModel> barRods;

  const BarChartGroupViewModel({required this.control, required this.barRods});

  static BarChartGroupViewModel fromStore(
      Store<AppState> store, Control control) {
    return BarChartGroupViewModel(
        control: control,
        barRods: store.state.controls[control.id]!.childIds
            .map((childId) => store.state.controls[childId])
            .whereNotNull()
            .where((c) => c.isVisible)
            .map((c) => BarChartRodViewModel.fromStore(store, c))
            .toList());
  }

  @override
  List<Object?> get props => [control, barRods];
}
