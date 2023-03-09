import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';
import 'linechart_axis_label_view_model.dart';

class LineChartAxisViewModel extends Equatable {
  final Control control;
  final Control? title;
  final Map<double, Control> labels;

  const LineChartAxisViewModel(
      {required this.control, required this.title, required this.labels});

  static LineChartAxisViewModel fromStore(
      Store<AppState> store, Control control) {
    var children = store.state.controls[control.id]!.childIds
        .map((childId) => store.state.controls[childId])
        .whereNotNull()
        .where((c) => c.isVisible);

    return LineChartAxisViewModel(
        control: control,
        title: children.where((c) => c.name == "t").firstOrNull,
        labels: {
          for (var e in children
              .where((c) => c.name == "l")
              .map((c) => LineChartAxisLabelViewModel.fromStore(store, c))
              .where((c) => c.control != null))
            e.value: e.control!
        });
  }

  @override
  List<Object?> get props => [control, title, labels];
}
