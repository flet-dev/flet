import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import '../models/piechart_section_view_model.dart';
import 'app_state.dart';
import 'control.dart';

class PieChartViewModel extends Equatable {
  final Control control;
  final List<PieChartSectionViewModel> sections;
  final dynamic dispatch;

  const PieChartViewModel(
      {required this.control, required this.sections, required this.dispatch});

  static PieChartViewModel fromStore(
      Store<AppState> store, Control control, List<Control> children) {
    return PieChartViewModel(
        control: control,
        sections: children
            .where((c) => c.type == "section" && c.isVisible)
            .map((c) => PieChartSectionViewModel.fromStore(store, c))
            .toList(),
        dispatch: store.dispatch);
  }

  @override
  List<Object?> get props => [control, sections, dispatch];
}
