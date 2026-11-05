import Cocoa
import FlutterMacOS
import window_manager

/// Renders with Skia instead of Flutter's default, Impeller, when
/// FLET_NO_IMPELLER is "1", "true" or "yes" (any case) at startup. Apps built
/// with `flet build --no-impeller` already render with Skia through the
/// FLTEnableImpeller Info.plist key.
///
/// The macOS engine takes the renderer only from the FLTEnableImpeller
/// Info.plist key, and release builds ignore engine switches from the
/// environment. So this replaces the engine's internal
/// `-[FlutterDartProject enableImpeller]` getter, which reads that key, before
/// the first engine starts. Subclassing `FlutterDartProject` instead would move
/// its ICU data lookup to the app bundle and break text segmentation.
private func disableImpellerIfRequested() {
  guard
    let value = ProcessInfo.processInfo.environment["FLET_NO_IMPELLER"],
    ["1", "true", "yes"].contains(value.lowercased())
  else { return }
  guard
    let method = class_getInstanceMethod(
      FlutterDartProject.self, NSSelectorFromString("enableImpeller"))
  else {
    NSLog("FLET_NO_IMPELLER is set, but this Flutter engine can't be switched to Skia.")
    return
  }
  let skia: @convention(block) (AnyObject) -> Bool = { _ in false }
  method_setImplementation(method, imp_implementationWithBlock(skia))
}

class MainFlutterWindow: NSWindow {
  override func awakeFromNib() {
    disableImpellerIfRequested()
    let flutterViewController = FlutterViewController()
    let windowFrame = self.frame
    self.contentViewController = flutterViewController
    self.setFrame(windowFrame, display: true)

    RegisterGeneratedPlugins(registry: flutterViewController)

    super.awakeFromNib()
  }

  override public func order(_ place: NSWindow.OrderingMode, relativeTo otherWin: Int) {
    super.order(place, relativeTo: otherWin)
    hiddenWindowAtLaunch()
  }
}
