import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';

/// Bridges an embedded app's routing to the host `FletApp` control that hosts
/// it.
///
/// The embedded app's [PageControl] is built deep inside the widget subtree
/// that `FletAppControl` returns, and the two sides never share a backend - the
/// guest speaks its own protocol on its own channel. An inherited widget is the
/// one thing they do share, so it carries the route across the boundary:
///
///  * host to guest - [route] is the route the host wants the guest on. The
///    embedded page pushes it through its local route information provider when
///    it differs from where the guest currently is.
///  * guest to host - [onRouteChanged] fires when the guest navigates itself,
///    so the host control can write the new route back and raise its event.
///
/// Both directions are guarded on equality, so a round trip settles instead of
/// looping. A host `PageControl` sits *above* `FletAppControl` and so never
/// sees this scope; with nested embedded apps the innermost one wins, which is
/// what `dependOnInheritedWidgetOfExactType` gives us for free.
class EmbeddedAppScope extends InheritedWidget {
  /// Route the host wants the embedded app on, or null to leave it alone.
  final String? route;

  /// Called when the embedded app navigates itself.
  final ValueChanged<String> onRouteChanged;

  /// Simulated window state the host wants the guest to believe in - width,
  /// height, maximized and so on. Keys are `Window` property names.
  final Map<String, dynamic>? window;

  /// Called when the embedded app asks its window to do something: a method
  /// name (`close`, `maximize`, ...) or `set` with the properties it wrote.
  ///
  /// A request, not a command - the host is free to ignore actions it does not
  /// simulate, which is how "minimize is unsupported" is expressed.
  final void Function(String name, Map<String, dynamic> args) onWindowAction;

  /// Called when the embedded app sets `page.title`.
  ///
  /// A guest's title belongs to the fake window its host draws around it, not
  /// to the real OS window - the window service, which is what would otherwise
  /// apply it, is suppressed for embedded pages.
  final ValueChanged<String> onTitleChanged;

  const EmbeddedAppScope({
    super.key,
    required this.route,
    required this.window,
    required this.onRouteChanged,
    required this.onTitleChanged,
    required this.onWindowAction,
    required super.child,
  });

  static EmbeddedAppScope? maybeOf(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<EmbeddedAppScope>();

  @override
  bool updateShouldNotify(EmbeddedAppScope oldWidget) =>
      route != oldWidget.route || !mapEquals(window, oldWidget.window);
}
