import Flutter
import UIKit
#if canImport(flutter_local_notifications)
import UserNotifications
import flutter_local_notifications
#endif

@main
@objc class AppDelegate: FlutterAppDelegate, FlutterImplicitEngineDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    #if canImport(flutter_local_notifications)
    UNUserNotificationCenter.current().delegate = self
    #endif
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }

  func didInitializeImplicitFlutterEngine(_ engineBridge: FlutterImplicitEngineBridge) {
    #if canImport(flutter_local_notifications)
    FlutterLocalNotificationsPlugin.setPluginRegistrantCallback { registry in
      GeneratedPluginRegistrant.register(with: registry)
    }
    #endif
    GeneratedPluginRegistrant.register(with: engineBridge.pluginRegistry)
  }
}
