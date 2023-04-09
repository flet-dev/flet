import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'barchart_group_view_model.dart';
import 'chart_axis_view_model.dart';
import 'control.dart';

class BarChartViewModel extends Equatable {
  final Control control;
  final ChartAxisViewModel? leftAxis;
  final ChartAxisViewModel? topAxis;
  final ChartAxisViewModel? rightAxis;
  final ChartAxisViewModel? bottomAxis;
  final List<BarChartGroupViewModel> barGroups;
  final dynamic dispatch;

  const BarChartViewModel(
      {required this.control,
      required this.leftAxis,
      required this.topAxis,
      required this.rightAxis,
      required this.bottomAxis,
      required this.barGroups,
      required this.dispatch});

  static BarChartViewModel fromStore(
      Store<AppState> store, Control control, List<Control> children) {
    var leftAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "l" && c.isVisible);
    var topAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "t" && c.isVisible);
    var rightAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "r" && c.isVisible);
    var bottomAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "b" && c.isVisible);
    return BarChartViewModel(
        control: control,
        leftAxis: leftAxisCtrls.isNotEmpty
            ? ChartAxisViewModel.fromStore(store, leftAxisCtrls.first)
            : null,
        topAxis: topAxisCtrls.isNotEmpty
            ? ChartAxisViewModel.fromStore(store, topAxisCtrls.first)
            : null,
        rightAxis: rightAxisCtrls.isNotEmpty
            ? ChartAxisViewModel.fromStore(store, rightAxisCtrls.first)
            : null,
        bottomAxis: bottomAxisCtrls.isNotEmpty
            ? ChartAxisViewModel.fromStore(store, bottomAxisCtrls.first)
            : null,
        barGroups: children
            .where((c) => c.type == "group" && c.isVisible)
            .map((c) => BarChartGroupViewModel.fromStore(store, c))
            .toList(),
        dispatch: store.dispatch);
  }

  @override
  List<Object?> get props =>
      [control, leftAxis, rightAxis, topAxis, bottomAxis, barGroups, dispatch];
}
