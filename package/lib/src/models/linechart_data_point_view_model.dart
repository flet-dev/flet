import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class LineChartDataPointViewModel extends Equatable {
  final Control control;
  final double x;
  final double y;
  final String? tooltip;

  const LineChartDataPointViewModel(
      {required this.control,
      required this.x,
      required this.y,
      required this.tooltip});

  static LineChartDataPointViewModel fromStore(
      Store<AppState> store, Control control) {
    return LineChartDataPointViewModel(
        control: control,
        x: control.attrDouble("x")!,
        y: control.attrDouble("y")!,
        tooltip: control.attrString("tooltip"));
  }

  @override
  List<Object?> get props => [control];
}
