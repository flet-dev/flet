import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';
import 'control_type.dart';

class RouteViewModel extends Equatable {
  final Control control;
  final List<Control> children;

  const RouteViewModel({required this.control, required this.children});

  static RouteViewModel? fromStore(Store<AppState> store, String? routeName) {
    var routeCtrl = store.state.controls.values.where((c) =>
        c.pid == "page" &&
        c.type == ControlType.view &&
        c.attrString("name", "")! == routeName);

    if (routeCtrl.isEmpty) {
      return null;
    }

    return RouteViewModel(
        control: routeCtrl.first,
        children: routeCtrl.first.childIds
            .map((childId) => store.state.controls[childId]!)
            .toList());
  }

  @override
  List<Object?> get props => [control, children];
}
