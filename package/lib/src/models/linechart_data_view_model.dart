import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';
import 'linechart_data_point_view_model.dart';

class LineChartDataViewModel extends Equatable {
  final Control control;
  final List<LineChartDataPointViewModel> dataPoints;

  const LineChartDataViewModel(
      {required this.control, required this.dataPoints});

  static LineChartDataViewModel fromStore(
      Store<AppState> store, Control control) {
    return LineChartDataViewModel(
        control: control,
        dataPoints: store.state.controls[control.id]!.childIds
            .map((childId) => store.state.controls[childId])
            .whereNotNull()
            .where((c) => c.isVisible)
            .map((c) => LineChartDataPointViewModel(
                x: c.attrDouble("x")!, y: c.attrDouble("y")!))
            .toList());
  }

  @override
  List<Object?> get props => [control, dataPoints];
}
