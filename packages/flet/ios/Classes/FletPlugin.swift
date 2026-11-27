import Flutter
import UIKit
import AuthenticationServices

public class FletPlugin: NSObject, FlutterPlugin {
  public static func register(with registrar: FlutterPluginRegistrar) {
    let channel = FlutterMethodChannel(name: "dev.flet/web_auth", binaryMessenger: registrar.messenger())
    let instance = FletWebAuthPlugin()
    registrar.addMethodCallDelegate(instance, channel: channel)
  }
}

final class FletWebAuthPlugin: NSObject, FlutterPlugin, ASWebAuthenticationPresentationContextProviding {
  private var session: ASWebAuthenticationSession?
  private var pendingResult: FlutterResult?

  public static func register(with registrar: FlutterPluginRegistrar) {
    // Registered via FletPlugin.
  }

  public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
    if call.method == "cancel" {
      session?.cancel()
      session = nil
      if let pending = pendingResult {
        pending([
          "error": "cancelled",
          "error_description": "WebAuth cancelled.",
        ])
        pendingResult = nil
      }
      result(nil)
      return
    }

    guard call.method == "authenticate" else {
      result(FlutterMethodNotImplemented)
      return
    }

    guard let args = call.arguments as? [String: Any],
          let urlString = args["url"] as? String,
          let url = URL(string: urlString) else {
      result([
        "error": "invalid_arguments",
        "error_description": "Missing or invalid url.",
      ])
      return
    }

    var scheme = args["callback_scheme"] as? String
    if scheme == nil || scheme!.isEmpty {
      if let redirect = args["redirect_url"] as? String, let redirectURL = URL(string: redirect) {
        scheme = redirectURL.scheme
      }
    }
    guard let callbackScheme = scheme, !callbackScheme.isEmpty else {
      result([
        "error": "invalid_redirect_url",
        "error_description": "callback_scheme / redirect_url scheme is required.",
      ])
      return
    }

    if pendingResult != nil {
      result([
        "error": "concurrent_authenticate",
        "error_description": "Another WebAuth call is in progress.",
      ])
      return
    }

    let ephemeral = (args["ephemeral"] as? Bool) ?? false
    pendingResult = result

    let authSession = ASWebAuthenticationSession(
      url: url,
      callbackURLScheme: callbackScheme
    ) { [weak self] callbackURL, error in
      guard let self = self else { return }
      defer {
        self.session = nil
        self.pendingResult = nil
      }
      if let error = error as? ASWebAuthenticationSessionError,
         error.code == .canceledLogin {
        self.pendingResult?([
          "error": "cancelled",
          "error_description": "User cancelled authorization.",
        ])
        return
      }
      if let error = error {
        self.pendingResult?([
          "error": "authenticate_failed",
          "error_description": error.localizedDescription,
        ])
        return
      }
      guard let callbackURL = callbackURL else {
        self.pendingResult?([
          "error": "authenticate_failed",
          "error_description": "ASWebAuthenticationSession returned no callback URL.",
        ])
        return
      }
      self.pendingResult?([
        "callback_url": callbackURL.absoluteString,
      ])
    }
    authSession.prefersEphemeralWebBrowserSession = ephemeral
    authSession.presentationContextProvider = self
    session = authSession
    if !authSession.start() {
      pendingResult?([
        "error": "authenticate_failed",
        "error_description": "Failed to start ASWebAuthenticationSession.",
      ])
      pendingResult = nil
      session = nil
    }
  }

  public func presentationAnchor(for session: ASWebAuthenticationSession) -> ASPresentationAnchor {
    if let scene = UIApplication.shared.connectedScenes
      .compactMap({ $0 as? UIWindowScene })
      .first(where: { $0.activationState == .foregroundActive }),
       let window = scene.windows.first(where: { $0.isKeyWindow }) {
      return window
    }
    return UIApplication.shared.windows.first { $0.isKeyWindow } ?? ASPresentationAnchor()
  }
}
