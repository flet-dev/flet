import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class BarChartRodStackItemViewModel extends Equatable {
  final Control control;

  const BarChartRodStackItemViewModel({required this.control});

  static BarChartRodStackItemViewModel fromStore(
      Store<AppState> store, Control control) {
    return BarChartRodStackItemViewModel(control: control);
  }

  @override
  List<Object?> get props => [control];
}
