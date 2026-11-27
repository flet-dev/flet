package dev.flet.flet;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.net.Uri;

import androidx.activity.ComponentActivity;
import androidx.activity.result.ActivityResultLauncher;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.browser.auth.AuthTabIntent;
import androidx.browser.customtabs.CustomTabsClient;
import androidx.browser.customtabs.CustomTabsIntent;

import java.util.HashMap;
import java.util.Map;

import io.flutter.embedding.engine.plugins.FlutterPlugin;
import io.flutter.embedding.engine.plugins.activity.ActivityAware;
import io.flutter.embedding.engine.plugins.activity.ActivityPluginBinding;
import io.flutter.plugin.common.MethodCall;
import io.flutter.plugin.common.MethodChannel;
import io.flutter.plugin.common.MethodChannel.MethodCallHandler;
import io.flutter.plugin.common.MethodChannel.Result;
import io.flutter.plugin.common.PluginRegistry;

/**
 * Platform WebAuth: open a sign-in URL and return the redirect callback URL.
 * No OAuth protocol logic (PKCE/state/token) — that stays in Python.
 */
public class FletWebAuthPlugin
    implements FlutterPlugin, MethodCallHandler, ActivityAware, PluginRegistry.ActivityResultListener {

  private static final String CHANNEL = "dev.flet/web_auth";
  private static final int RC_CUSTOM_TAB = 65042;

  private MethodChannel channel;
  private Activity activity;
  private ActivityPluginBinding activityBinding;
  @Nullable private ActivityResultLauncher<Intent> authTabLauncher;
  @Nullable private PendingAuth pending;

  @Override
  public void onAttachedToEngine(@NonNull FlutterPluginBinding binding) {
    channel = new MethodChannel(binding.getBinaryMessenger(), CHANNEL);
    channel.setMethodCallHandler(this);
  }

  @Override
  public void onDetachedFromEngine(@NonNull FlutterPluginBinding binding) {
    if (channel != null) {
      channel.setMethodCallHandler(null);
      channel = null;
    }
  }

  @Override
  public void onAttachedToActivity(@NonNull ActivityPluginBinding binding) {
    activityBinding = binding;
    activity = binding.getActivity();
    binding.addActivityResultListener(this);
    if (activity instanceof ComponentActivity) {
      authTabLauncher =
          AuthTabIntent.registerActivityResultLauncher(
              (ComponentActivity) activity, this::onAuthTabResult);
    }
  }

  @Override
  public void onDetachedFromActivityForConfigChanges() {
    teardownActivity();
  }

  @Override
  public void onReattachedToActivityForConfigChanges(@NonNull ActivityPluginBinding binding) {
    onAttachedToActivity(binding);
  }

  @Override
  public void onDetachedFromActivity() {
    teardownActivity();
  }

  private void teardownActivity() {
    if (activityBinding != null) {
      activityBinding.removeActivityResultListener(this);
      activityBinding = null;
    }
    activity = null;
    authTabLauncher = null;
    if (pending != null) {
      finishPending(errorMap("cancelled", "Activity detached during WebAuth."));
    }
  }

  @Override
  public void onMethodCall(@NonNull MethodCall call, @NonNull Result result) {
    if ("cancel".equals(call.method)) {
      if (pending != null) {
        finishPending(errorMap("cancelled", "WebAuth cancelled."));
      }
      result.success(null);
      return;
    }
    if (!"authenticate".equals(call.method)) {
      result.notImplemented();
      return;
    }
    if (activity == null) {
      result.success(errorMap("null_activity", "No Android activity for WebAuth."));
      return;
    }
    if (pending != null) {
      result.success(errorMap("concurrent_authenticate", "Another WebAuth call is in progress."));
      return;
    }

    Map<String, Object> args = call.arguments();
    try {
      String url = requireString(args, "url");
      String redirectUrl = requireString(args, "redirect_url");
      String scheme = (String) args.get("callback_scheme");
      if (scheme == null || scheme.isEmpty()) {
        Uri redirectUri = Uri.parse(redirectUrl);
        scheme = redirectUri.getScheme();
      }
      if (scheme == null || scheme.isEmpty()) {
        result.success(errorMap("invalid_redirect_url", "redirect_url must include a URI scheme."));
        return;
      }
      boolean ephemeral = Boolean.TRUE.equals(args.get("ephemeral"));
      pending = new PendingAuth(result, scheme);

      if (authTabLauncher != null && isAuthTabSupported()) {
        AuthTabIntent.Builder builder = new AuthTabIntent.Builder();
        if (ephemeral) {
          builder.setEphemeralBrowsingEnabled(true);
        }
        AuthTabIntent authTabIntent = builder.build();
        authTabIntent.launch(authTabLauncher, Uri.parse(url), scheme);
        return;
      }

      // Fallback: Custom Tab (JS-initiated custom-scheme hops may fail — Auth Tab preferred).
      CustomTabsIntent customTabsIntent = new CustomTabsIntent.Builder().build();
      customTabsIntent.intent.setData(Uri.parse(url));
      try {
        activity.startActivityForResult(customTabsIntent.intent, RC_CUSTOM_TAB);
      } catch (ActivityNotFoundException ex) {
        finishPending(errorMap("no_browser_available", "No suitable browser is available."));
      }
    } catch (Exception ex) {
      pending = null;
      result.success(
          errorMap(
              "authenticate_failed",
              ex.getLocalizedMessage() != null ? ex.getLocalizedMessage() : ex.toString()));
    }
  }

  private boolean isAuthTabSupported() {
    if (activity == null) {
      return false;
    }
    String packageName =
        CustomTabsClient.getPackageName(activity, null, true /* ignore default */);
    if (packageName == null) {
      packageName = CustomTabsClient.getPackageName(activity, null);
    }
    if (packageName == null) {
      return false;
    }
    return CustomTabsClient.isAuthTabSupported(activity, packageName);
  }

  private void onAuthTabResult(AuthTabIntent.AuthResult authResult) {
    if (pending == null) {
      return;
    }
    int code = authResult.resultCode;
    if (code == AuthTabIntent.RESULT_OK) {
      Uri resultUri = authResult.resultUri;
      if (resultUri == null) {
        finishPending(errorMap("authenticate_failed", "Auth Tab returned no redirect URI."));
        return;
      }
      Map<String, Object> map = new HashMap<>();
      map.put("callback_url", resultUri.toString());
      finishPending(map);
      return;
    }
    if (code == AuthTabIntent.RESULT_CANCELED) {
      finishPending(errorMap("cancelled", "User cancelled authorization."));
      return;
    }
    finishPending(errorMap("authenticate_failed", "Auth Tab failed with result code " + code + "."));
  }

  @Override
  public boolean onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
    if (requestCode != RC_CUSTOM_TAB || pending == null) {
      return false;
    }
    // Custom Tab close without a captured redirect — treat as cancel.
    // (Redirect delivery for Custom Tab requires a dedicated callback activity
    // registered at build time; Auth Tab is the preferred path.)
    if (data != null && data.getData() != null) {
      Map<String, Object> map = new HashMap<>();
      map.put("callback_url", data.getData().toString());
      finishPending(map);
      return true;
    }
    finishPending(errorMap("cancelled", "User cancelled authorization."));
    return true;
  }

  private static String requireString(Map<String, Object> args, String key) {
    Object value = args.get(key);
    if (!(value instanceof String) || ((String) value).isEmpty()) {
      throw new IllegalArgumentException("Missing authenticate argument: " + key);
    }
    return (String) value;
  }

  private void finishPending(Map<String, Object> payload) {
    PendingAuth current = pending;
    pending = null;
    if (current != null) {
      current.result.success(payload);
    }
  }

  private static Map<String, Object> errorMap(String error, String description) {
    Map<String, Object> map = new HashMap<>();
    map.put("error", error);
    map.put("error_description", description);
    return map;
  }

  private static final class PendingAuth {
    final Result result;
    final String scheme;

    PendingAuth(Result result, String scheme) {
      this.result = result;
      this.scheme = scheme;
    }
  }
}
