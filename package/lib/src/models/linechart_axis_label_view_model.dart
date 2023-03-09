import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class LineChartAxisLabelViewModel extends Equatable {
  final double value;
  final Control? control;

  const LineChartAxisLabelViewModel(
      {required this.value, required this.control});

  static LineChartAxisLabelViewModel fromStore(
      Store<AppState> store, Control control) {
    return LineChartAxisLabelViewModel(
        value: control.attrDouble("value")!,
        control: store.state.controls[control.id]!.childIds
            .map((childId) => store.state.controls[childId])
            .whereNotNull()
            .where((c) => c.isVisible)
            .firstOrNull);
  }

  @override
  List<Object?> get props => [value, control];
}
