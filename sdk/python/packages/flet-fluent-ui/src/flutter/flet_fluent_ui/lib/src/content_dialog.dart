import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

/// A `flet_fluent_ui.ContentDialog`.
///
/// Like Flet's AlertDialog, it renders nothing in place: when `open` becomes
/// true it pushes fluent_ui's dialog route, and when the route is gone it sets
/// `open` to false and triggers `dismiss`.
class FluentContentDialogControl extends StatefulWidget {
  final Control control;

  const FluentContentDialogControl({super.key, required this.control});

  @override
  State<FluentContentDialogControl> createState() =>
      _FluentContentDialogControlState();
}

class _FluentContentDialogControlState
    extends State<FluentContentDialogControl> {
  // The route pushed for this dialog, so closing it from Python removes this
  // route rather than whatever route is on top.
  ModalRoute? _route;

  Control get control => widget.control;

  void _show(BuildContext themedContext) {
    // The route is built outside this control's widget tree: fluent_ui
    // carries the FluentTheme over, but not the localizations, so the content
    // is wrapped again. It rebuilds itself when the control changes.
    Widget builder(BuildContext context) {
      _route ??= ModalRoute.of(context);
      return withFluentTheme(
        context,
        ListenableBuilder(
          listenable: control,
          builder: (context, _) {
            final actions = control.buildWidgets("actions");
            return ContentDialog(
              title: control.buildTextOrWidget("title"),
              content: control.buildTextOrWidget("content"),
              actions: actions.isEmpty ? null : actions,
            );
          },
        ),
      );
    }

    showDialog<void>(
      context: themedContext,
      barrierDismissible: !control.getBool("modal", true)!,
      useRootNavigator: false,
      builder: builder,
    ).then((_) {
      final route = _route;
      _route = null;
      // The future completes on pop, before the exit animation ends; report
      // the dismissal once the route has fully gone.
      (route?.completed ?? Future.value()).then((_) {
        control.updateProperties({"_open": false}, python: false);
        control.updateProperties({"open": false});
        control.triggerEvent("dismiss");
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentContentDialog build: ${control.id}");

    final open = control.getBool("open", false)!;
    final lastOpen = control.getBool("_open", false)!;

    // showDialog reads FluentLocalizations and captures the FluentTheme from
    // the context it is called with, so it is called with a context below
    // both.
    return withFluentTheme(
      context,
      Builder(
        builder: (themedContext) {
          if (open && !lastOpen) {
            control.updateProperties({"_open": true}, python: false);
            WidgetsBinding.instance.addPostFrameCallback((_) {
              if (mounted) _show(themedContext);
            });
          } else if (!open && lastOpen) {
            control.updateProperties({"_open": false}, python: false);
            final route = _route;
            if (route != null) {
              WidgetsBinding.instance.addPostFrameCallback(
                (_) => closeModalRoute(route),
              );
            }
          }
          return const SizedBox.shrink();
        },
      ),
    );
  }
}
