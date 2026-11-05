import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

/// A `flet_shadcn_ui.Dialog` or `flet_shadcn_ui.Sheet`.
///
/// Like Flet's AlertDialog, it renders nothing in place: when `open` becomes
/// true it pushes shadcn's dialog or sheet route, and when the route is gone
/// it sets `open` to false and triggers `dismiss`.
class ShadRouteOverlayControl extends StatefulWidget {
  final Control control;
  final bool sheet;

  const ShadRouteOverlayControl({
    super.key,
    required this.control,
    required this.sheet,
  });

  @override
  State<ShadRouteOverlayControl> createState() =>
      _ShadRouteOverlayControlState();
}

class _ShadRouteOverlayControlState extends State<ShadRouteOverlayControl> {
  // The route pushed for this overlay, so closing it from Python removes this
  // route rather than whatever route is on top.
  ModalRoute? _route;

  Control get control => widget.control;

  Widget _buildContent(BuildContext context) {
    final title = control.buildTextOrWidget("title");
    final description = control.buildTextOrWidget("description");
    final child = control.buildWidget("content");
    final actions = control.buildWidgets("actions");
    if (widget.sheet) {
      return ShadSheet(
        title: title,
        description: description,
        actions: actions,
        child: child,
      );
    }
    return control.getString("variant") == "alert"
        ? ShadDialog.alert(
            title: title,
            description: description,
            actions: actions,
            child: child,
          )
        : ShadDialog(
            title: title,
            description: description,
            actions: actions,
            child: child,
          );
  }

  void _show(BuildContext themedContext) {
    final modal = control.getBool("modal", false)!;

    // The route is built outside this control's widget tree, so it gets its
    // own theme and rebuilds itself when the control changes.
    Widget builder(BuildContext context) {
      _route ??= ModalRoute.of(context);
      return withShadTheme(
        context,
        ListenableBuilder(
          listenable: control,
          builder: (context, _) => _buildContent(context),
        ),
      );
    }

    final future = widget.sheet
        ? showShadSheet<void>(
            context: themedContext,
            side: parseEnum(
              ShadSheetSide.values,
              control.getString("side"),
              ShadSheetSide.bottom,
            ),
            isDismissible: !modal,
            builder: builder,
          )
        : showShadDialog<void>(
            context: themedContext,
            barrierDismissible: !modal,
            useRootNavigator: false,
            builder: builder,
          );

    future.then((_) {
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
    debugPrint(
      "${widget.sheet ? "ShadSheet" : "ShadDialog"} build: "
      "${control.id}",
    );

    final open = control.getBool("open", false)!;
    final lastOpen = control.getBool("_open", false)!;

    // showShadSheet/showShadDialog read ShadTheme from the context they are
    // called with, so they are called with a context below a ShadTheme.
    return withShadTheme(
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

/// The ShadToaster and ShadSonner that toasts are shown in.
///
/// ShadApp puts these at the root of the app; Flet apps have none, and toast
/// controls come and go, so one shared host is inserted into the root overlay
/// the first time a toast is shown.
class _ToastHost {
  static final _hosts = Expando<_ToastHost>();

  final toasterKey = GlobalKey<ShadToasterState>();
  final sonnerKey = GlobalKey<ShadSonnerState>();

  /// The toast control state whose toast the toaster shows; the toaster shows
  /// one toast at a time.
  _ShadToastControlState? toastOwner;

  _ToastHost._(OverlayState overlay) {
    overlay.insert(
      OverlayEntry(
        builder: (context) => withShadTheme(
          context,
          ShadToaster(
            key: toasterKey,
            child: ShadSonner(key: sonnerKey, child: const SizedBox.expand()),
          ),
        ),
      ),
    );
  }

  /// Returns the host for [context]'s root overlay, creating it if needed.
  /// A new host is usable after the next frame.
  static _ToastHost of(BuildContext context) {
    final overlay = Overlay.of(context, rootOverlay: true);
    return _hosts[overlay] ??= _ToastHost._(overlay);
  }
}

/// A `flet_shadcn_ui.Toast` (one at a time) or `flet_shadcn_ui.Sonner`
/// (stacked).
///
/// shadcn_ui does not report when a toast goes away, so this control runs the
/// duration timer and provides the close button itself, which lets it set
/// `open` to false and trigger `dismiss` however the toast disappears.
class ShadToastControl extends StatefulWidget {
  final Control control;
  final bool sonner;

  const ShadToastControl({
    super.key,
    required this.control,
    required this.sonner,
  });

  @override
  State<ShadToastControl> createState() => _ShadToastControlState();
}

class _ShadToastControlState extends State<ShadToastControl> {
  _ToastHost? _host;
  Object? _sonnerId;
  Timer? _timer;
  bool _showing = false;

  Control get control => widget.control;

  bool get _destructive => control.getString("variant") == "destructive";

  @override
  void dispose() {
    _timer?.cancel();
    if (_showing) _hide();
    super.dispose();
  }

  Widget _closeButton() {
    return Builder(
      builder: (context) {
        final colorScheme = ShadTheme.of(context).colorScheme;
        final foreground = _destructive
            ? colorScheme.destructiveForeground
            : colorScheme.foreground;
        return ShadIconButton.ghost(
          icon: const Icon(LucideIcons.x, size: 16),
          width: 20,
          height: 20,
          padding: EdgeInsets.zero,
          foregroundColor: foreground.withValues(alpha: .5),
          hoverBackgroundColor: const Color(0x00000000),
          hoverForegroundColor: foreground,
          pressedForegroundColor: foreground,
          onPressed: () => _finish(hide: true),
        );
      },
    );
  }

  ShadToast _buildToast(Duration duration) {
    final variant = _destructive
        ? ShadToastVariant.destructive
        : ShadToastVariant.primary;
    final action = control.buildWidget("action");
    return ShadToast.raw(
      variant: variant,
      id: _sonnerId,
      title: control.buildTextOrWidget("title"),
      description: control.buildTextOrWidget("description"),
      action: action,
      closeIcon: _closeButton(),
      // The close icon sits 8px from the top-end corner and is 20px wide,
      // but shadcn_ui leaves only 32px of end padding, so an action button
      // would end 4px from it and overlap it vertically. Leave room for it.
      padding: action != null
          ? const EdgeInsetsDirectional.fromSTEB(24, 24, 44, 24)
          : null,
      duration: duration,
    );
  }

  void _show() {
    final host = _host!;
    final duration = control.getDuration(
      "duration",
      const Duration(seconds: 5),
    )!;
    if (widget.sonner) {
      final sonner = host.sonnerKey.currentState;
      if (sonner == null) return;
      _sonnerId = UniqueKey();
      sonner.show(_buildToast(duration));
    } else {
      final toaster = host.toasterKey.currentState;
      if (toaster == null) return;
      // The toaster shows one toast: the one it replaces is dismissed.
      final previous = host.toastOwner;
      host.toastOwner = this;
      previous?._finish(hide: false);
      toaster.show(_buildToast(duration));
    }
    _showing = true;
    _timer = Timer(duration, () => _finish(hide: true));
  }

  void _hide() {
    final host = _host;
    if (host == null) return;
    if (widget.sonner) {
      host.sonnerKey.currentState?.hide(_sonnerId);
    } else if (host.toastOwner == this) {
      host.toastOwner = null;
      host.toasterKey.currentState?.hide();
    }
  }

  /// Takes the toast away (unless it is already gone) and reports dismissal.
  void _finish({required bool hide}) {
    if (!_showing) return;
    _showing = false;
    _timer?.cancel();
    if (hide) {
      _hide();
    } else if (_host?.toastOwner == this) {
      _host!.toastOwner = null;
    }
    control.updateProperties({"_open": false}, python: false);
    control.updateProperties({"open": false});
    control.triggerEvent("dismiss");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(
      "${widget.sonner ? "ShadSonner" : "ShadToast"} build: "
      "${control.id}",
    );

    final open = control.getBool("open", false)!;
    final lastOpen = control.getBool("_open", false)!;

    if (open && !lastOpen) {
      control.updateProperties({"_open": true}, python: false);
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (!mounted) return;
        final isNew =
            _ToastHost._hosts[Overlay.of(context, rootOverlay: true)] == null;
        _host = _ToastHost.of(context);
        if (isNew) {
          // A just-inserted host is built in the next frame.
          WidgetsBinding.instance.addPostFrameCallback((_) {
            if (mounted) _show();
          });
          WidgetsBinding.instance.scheduleFrame();
        } else {
          _show();
        }
      });
    } else if (!open && lastOpen) {
      WidgetsBinding.instance.addPostFrameCallback((_) => _finish(hide: true));
    }
    return const SizedBox.shrink();
  }
}
