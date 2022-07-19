import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:flet_view/models/control_view_model.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';
import 'control_type.dart';

class RoutesViewModel extends Equatable {
  final Control page;
  final bool isLoading;
  final List<Control> offstageControls;
  final List<ControlViewModel> viewControls;

  const RoutesViewModel(
      {required this.page,
      required this.isLoading,
      required this.offstageControls,
      required this.viewControls});

  static RoutesViewModel fromStore(Store<AppState> store) {
    Control? offstageControl = store.state.controls["page"]!.childIds
        .map((childId) => store.state.controls[childId]!)
        .firstWhereOrNull((c) => c.type == ControlType.offstage);

    return RoutesViewModel(
        page: store.state.controls["page"]!,
        isLoading: store.state.isLoading,
        offstageControls: offstageControl != null
            ? store.state.controls[offstageControl.id]!.childIds
                .map((childId) => store.state.controls[childId]!)
                .where((c) => c.isVisible)
                .toList()
            : [],
        viewControls: store.state.controls["page"]!.childIds
            .map((childId) => store.state.controls[childId]!)
            .where((c) => c.type != ControlType.offstage && c.isVisible)
            .map((c) => ControlViewModel.fromStore(store, c.id))
            .toList());
  }

  @override
  List<Object?> get props => [page, isLoading, offstageControls, viewControls];
}
