import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class ChartAxisLabelViewModel extends Equatable {
  final double value;
  final Control? control;

  const ChartAxisLabelViewModel({required this.value, required this.control});

  static ChartAxisLabelViewModel fromStore(
      Store<AppState> store, Control control) {
    return ChartAxisLabelViewModel(
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
