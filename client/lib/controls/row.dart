import '../models/page_breakpoint_view_model.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import 'create_control.dart';

class RowControl extends StatelessWidget {
  final Control control;
  final List<Control> children;

  const RowControl({Key? key, required this.control, required this.children})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    // debugPrint("Row build: ${control.id}");
    // return Row(
    //     mainAxisAlignment: MainAxisAlignment.start,
    //     children:
    //         control.childIds.map((childId) => createControl(childId)).toList());

    return StoreConnector<AppState, PageBreakpointViewModel>(
        distinct: true,
        converter: (store) => PageBreakpointViewModel.fromStore(store),
        builder: (context, viewModel) {
          debugPrint(
              "Row build: ${control.id} with breakpoint: ${viewModel.breakpoint}");

          return Row(
            mainAxisAlignment: MainAxisAlignment.start,
            children: control.childIds
                .map((childId) => createControl(childId))
                .toList(),
          );
        });
  }
}
