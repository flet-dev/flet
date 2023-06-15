import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class RoutesViewModel extends Equatable {
  final Control page;
  final bool isLoading;
  final String error;
  final List<Control> offstageControls;
  final List<Control> views;

  const RoutesViewModel(
      {required this.page,
      required this.isLoading,
      required this.error,
      required this.offstageControls,
      required this.views});

  static RoutesViewModel fromStore(Store<AppState> store) {
    Control? offstageControl = store.state.controls["page"]!.childIds
        .map((childId) => store.state.controls[childId]!)
        .firstWhereOrNull((c) => c.type == "offstage");

    return RoutesViewModel(
        page: store.state.controls["page"]!,
        isLoading: store.state.isLoading,
        error: store.state.error,
        offstageControls: offstageControl != null
            ? store.state.controls[offstageControl.id]!.childIds
                .map((childId) => store.state.controls[childId]!)
                .where((c) => c.isVisible)
                .toList()
            : [],
        views: store.state.controls["page"]!.childIds
            .map((childId) => store.state.controls[childId]!)
            .where((c) => c.type != "offstage" && c.isVisible)
            .toList());
  }

  @override
  List<Object?> get props => [page, isLoading, error, offstageControls, views];
}
