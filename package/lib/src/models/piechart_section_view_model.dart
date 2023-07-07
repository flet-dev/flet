import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class PieChartSectionViewModel extends Equatable {
  final Control control;
  final Control? badge;

  const PieChartSectionViewModel({required this.control, required this.badge});

  static PieChartSectionViewModel fromStore(
      Store<AppState> store, Control control) {
    var children = store.state.controls[control.id]!.childIds
        .map((childId) => store.state.controls[childId])
        .whereNotNull()
        .where((c) => c.isVisible);

    return PieChartSectionViewModel(
        control: control,
        badge: children.firstWhereOrNull((c) => c.name == "badge"));
  }

  @override
  List<Object?> get props => [control, badge];
}
