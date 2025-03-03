import UIKit
import Flutter
import awesome_notifications
import shared_preferences_ios

@main
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {

    GeneratedPluginRegistrant.register(with: self)

    // Register AwesomeNotifications Plugin for background actions
    SwiftAwesomeNotificationsPlugin.setPluginRegistrantCallback { registry in
        SwiftAwesomeNotificationsPlugin.register(
          with: registry.registrar(forPlugin: "io.flutter.plugins.awesomenotifications.AwesomeNotificationsPlugin")!)
        FLTSharedPreferencesPlugin.register(
          with: registry.registrar(forPlugin: "io.flutter.plugins.sharedpreferences.SharedPreferencesPlugin")!)
    }

    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}
