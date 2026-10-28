import UIKit
import Flutter
#if canImport(flutter_local_notifications)
import UserNotifications
import flutter_local_notifications
#endif

@main
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    #if canImport(flutter_local_notifications)
    UNUserNotificationCenter.current().delegate = self
    FlutterLocalNotificationsPlugin.setPluginRegistrantCallback { registry in
      GeneratedPluginRegistrant.register(with: registry)
    }
    #endif
    GeneratedPluginRegistrant.register(with: self)
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}
