import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';
import 'control_type.dart';

class RouteViewModel extends Equatable {
  final Control? control;
  final List<Control>? children;
  final bool isLoading;

  const RouteViewModel(
      {required this.control, required this.children, required this.isLoading});

  static RouteViewModel fromStore(Store<AppState> store, String? routeName) {
    var routeCtrl = store.state.controls.values.where((c) =>
        c.pid == "page" &&
        c.type == ControlType.view &&
        c.attrString("name", "")! == routeName);

    bool isLoading = store.state.isLoading;

    if (routeCtrl.isEmpty) {
      return RouteViewModel(
          control: null, children: null, isLoading: isLoading);
    }

    return RouteViewModel(
        control: routeCtrl.first,
        children: routeCtrl.first.childIds
            .map((childId) => store.state.controls[childId]!)
            .toList(),
        isLoading: isLoading);
  }

  @override
  List<Object?> get props => [control, children, isLoading];
}
