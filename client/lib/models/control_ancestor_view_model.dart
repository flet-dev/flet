import 'package:equatable/equatable.dart';
import 'package:flet_view/models/control_type.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class ControlAncestorViewModel extends Equatable {
  final Control? ancestor;
  final Function dispatch;

  const ControlAncestorViewModel(
      {required this.ancestor, required this.dispatch});

  static ControlAncestorViewModel fromStore(
      Store<AppState> store, String id, ControlType ancestorType) {
    Control? ancestor;
    String controlId = id;
    while (true) {
      String parentId = store.state.controls[controlId]!.pid;
      if (parentId == "") {
        break;
      }
      ancestor = store.state.controls[parentId]!;
      if (ancestor.type == ancestorType) {
        break;
      }
      controlId = ancestor.id;
    }

    return ControlAncestorViewModel(
        ancestor: ancestor, dispatch: store.dispatch);
  }

  @override
  List<Object?> get props => [ancestor];
}
