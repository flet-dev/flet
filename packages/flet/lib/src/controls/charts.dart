import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';

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
            .nonNulls
            .where((c) => c.isVisible)
            .firstOrNull);
  }

  @override
  List<Object?> get props => [value, control];
}

class ChartAxisViewModel extends Equatable {
  final Control control;
  final Control? title;
  final Map<double, Control> labels;

  const ChartAxisViewModel(
      {required this.control, required this.title, required this.labels});

  static ChartAxisViewModel fromStore(Store<AppState> store, Control control) {
    var children = store.state.controls[control.id]!.childIds
        .map((childId) => store.state.controls[childId])
        .nonNulls
        .where((c) => c.isVisible);

    return ChartAxisViewModel(
        control: control,
        title: children.where((c) => c.name == "t" && c.isVisible).firstOrNull,
        labels: {
          for (var e in children
              .where((c) => c.name == "l" && c.isVisible)
              .map((c) => ChartAxisLabelViewModel.fromStore(store, c))
              .where((c) => c.control != null))
            e.value: e.control!
        });
  }

  @override
  List<Object?> get props => [control, title, labels];
}
