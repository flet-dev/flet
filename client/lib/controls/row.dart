import '../models/page_breakpoint_view_model.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import 'create_control.dart';

class RowControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;

  const RowControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    bool disabled = control.isDisabled || parentDisabled;

    return StoreConnector<AppState, PageBreakpointViewModel>(
        distinct: true,
        converter: (store) => PageBreakpointViewModel.fromStore(store),
        builder: (context, viewModel) {
          debugPrint(
              "Row build: ${control.id} with breakpoint: ${viewModel.breakpoint}");

          return expandable(
              Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: control.childIds
                    .map((childId) => createControl(control, childId, disabled))
                    .toList(),
              ),
              control);
        });
  }
}
