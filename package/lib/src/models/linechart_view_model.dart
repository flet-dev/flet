import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';
import 'linechart_axis_view_model.dart';
import 'linechart_data_view_model.dart';

class LineChartViewModel extends Equatable {
  final Control control;
  final LineChartAxisViewModel? leftAxis;
  final LineChartAxisViewModel? topAxis;
  final LineChartAxisViewModel? rightAxis;
  final LineChartAxisViewModel? bottomAxis;
  final List<LineChartDataViewModel> dataSeries;
  final dynamic dispatch;

  const LineChartViewModel(
      {required this.control,
      required this.leftAxis,
      required this.topAxis,
      required this.rightAxis,
      required this.bottomAxis,
      required this.dataSeries,
      required this.dispatch});

  static LineChartViewModel fromStore(
      Store<AppState> store, Control control, List<Control> children) {
    var leftAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "l" && c.isVisible);
    var topAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "t" && c.isVisible);
    var rightAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "r" && c.isVisible);
    var bottomAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "b" && c.isVisible);
    return LineChartViewModel(
        control: control,
        leftAxis: leftAxisCtrls.isNotEmpty
            ? LineChartAxisViewModel.fromStore(store, leftAxisCtrls.first)
            : null,
        topAxis: topAxisCtrls.isNotEmpty
            ? LineChartAxisViewModel.fromStore(store, topAxisCtrls.first)
            : null,
        rightAxis: rightAxisCtrls.isNotEmpty
            ? LineChartAxisViewModel.fromStore(store, rightAxisCtrls.first)
            : null,
        bottomAxis: bottomAxisCtrls.isNotEmpty
            ? LineChartAxisViewModel.fromStore(store, bottomAxisCtrls.first)
            : null,
        dataSeries: children
            .where((c) => c.type == "data" && c.isVisible)
            .map((c) => LineChartDataViewModel.fromStore(store, c))
            .toList(),
        dispatch: store.dispatch);
  }

  @override
  List<Object?> get props =>
      [control, leftAxis, rightAxis, topAxis, bottomAxis, dataSeries, dispatch];
}
