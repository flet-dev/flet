/// The stage the app is currently at while booting.
enum BootStage {
  /// The app bundle is being unpacked and the runtime prepared. No Flet
  /// backend exists yet (desktop/mobile production startup).
  preparing,

  /// The Python runtime and the Flet app are starting up, until the first
  /// page is shown.
  startingUp,
}

/// The current boot status delivered to a boot screen widget.
///
/// A boot screen observes a [ValueListenable] of [BootStatus] to update its
/// visuals as the app progresses through the boot [stage], and to render an
/// error state when [error] is non-null.
class BootStatus {
  final BootStage stage;

  /// Non-null when startup/connection failed. The message is already
  /// formatted for display. A heading can be derived from [stage].
  final String? error;

  const BootStatus(this.stage, {this.error});

  @override
  bool operator ==(Object other) =>
      other is BootStatus && other.stage == stage && other.error == error;

  @override
  int get hashCode => Object.hash(stage, error);
}
