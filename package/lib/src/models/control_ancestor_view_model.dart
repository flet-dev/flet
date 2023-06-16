import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class ControlAncestorViewModel extends Equatable {
  final Control? ancestor;

  const ControlAncestorViewModel({required this.ancestor});

  static ControlAncestorViewModel fromStore(
      Store<AppState> store, String id, String ancestorType) {
    Control? ancestor;
    String controlId = id;
    while (true) {
      String parentId = store.state.controls[controlId]!.pid;
      if (parentId == "") {
        break;
      }
      ancestor = store.state.controls[parentId]!;
      if (ancestor.type.toLowerCase() == ancestorType.toLowerCase()) {
        break;
      }
      controlId = ancestor.id;
    }

    return ControlAncestorViewModel(ancestor: ancestor);
  }

  @override
  List<Object?> get props => [ancestor];
}
