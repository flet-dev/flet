package dev.flet.flet_appauth;

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

import net.openid.appauth.AppAuthConfiguration;
import net.openid.appauth.AuthorizationException;
import net.openid.appauth.AuthorizationRequest;
import net.openid.appauth.AuthorizationResponse;
import net.openid.appauth.AuthorizationService;
import net.openid.appauth.AuthorizationServiceConfiguration;
import net.openid.appauth.ResponseTypeValues;
import net.openid.appauth.browser.BrowserDenyList;
import net.openid.appauth.browser.VersionedBrowserMatcher;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
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
 * Android authorize path for flet-appauth.
 *
 * Prefers Chrome Auth Tab so custom-scheme OAuth redirects
 * ({@code flet://...}) are returned via callback. Standard Custom Tabs often
 * block that hop when the IdP navigates with JavaScript after passkey/consent
 * (no user gesture). Falls back to AppAuth in a full external browser when
 * Auth Tab is unavailable.
 */
public class FletAppauthPlugin
    implements FlutterPlugin, MethodCallHandler, ActivityAware, PluginRegistry.ActivityResultListener {

  private static final String CHANNEL = "dev.flet/flet_appauth";
  private static final int RC_EXTERNAL_BROWSER_AUTH = 65041;

  private MethodChannel channel;
  private Activity activity;
  private ActivityPluginBinding activityBinding;
  @Nullable private ActivityResultLauncher<Intent> authTabLauncher;
  @Nullable private PendingAuthorize pending;
  @Nullable private AuthorizationService externalBrowserAuthService;

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
    disposeExternalBrowserService();
  }

  @Override
  public void onMethodCall(@NonNull MethodCall call, @NonNull Result result) {
    if (!"authorize".equals(call.method)) {
      result.notImplemented();
      return;
    }
    if (activity == null) {
      result.success(errorMap("null_activity", "No Android activity for AppAuth authorize."));
      return;
    }
    if (pending != null) {
      result.success(errorMap("concurrent_authorize", "Another authorize call is already in progress."));
      return;
    }

    Map<String, Object> args = call.arguments();
    try {
      AuthorizationRequest request = buildAuthorizationRequest(args);
      String redirectScheme = Uri.parse(request.redirectUri.toString()).getScheme();
      if (redirectScheme == null || redirectScheme.isEmpty()) {
        result.success(errorMap("invalid_redirect_url", "redirect_url must include a URI scheme."));
        return;
      }

      pending = new PendingAuthorize(request, result);

      if (authTabLauncher != null && isAuthTabSupported()) {
        // Ephemeral Auth Tab does not share Chrome cookies with the normal
        // browser profile — required for provider-agnostic sign-out so the
        // next authorize cannot silently reuse an IdP SSO session.
        AuthTabIntent.Builder builder = new AuthTabIntent.Builder();
        if (Boolean.TRUE.equals(args.get("prefer_ephemeral_session"))) {
          builder.setEphemeralBrowsingEnabled(true);
        }
        AuthTabIntent authTabIntent = builder.build();
        authTabIntent.launch(authTabLauncher, request.toUri(), redirectScheme);
        return;
      }

      launchExternalBrowserAuthorize(request);
    } catch (Exception ex) {
      pending = null;
      result.success(
          errorMap("authorize_failed", ex.getLocalizedMessage() != null ? ex.getLocalizedMessage() : ex.toString()));
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

  private void launchExternalBrowserAuthorize(AuthorizationRequest request) {
    disposeExternalBrowserService();
    AppAuthConfiguration config =
        new AppAuthConfiguration.Builder()
            .setBrowserMatcher(
                new BrowserDenyList(
                    VersionedBrowserMatcher.CHROME_CUSTOM_TAB,
                    VersionedBrowserMatcher.SAMSUNG_CUSTOM_TAB,
                    VersionedBrowserMatcher.FIREFOX_CUSTOM_TAB))
            .build();
    externalBrowserAuthService = new AuthorizationService(activity, config);
    try {
      Intent authIntent = externalBrowserAuthService.getAuthorizationRequestIntent(request);
      activity.startActivityForResult(authIntent, RC_EXTERNAL_BROWSER_AUTH);
    } catch (ActivityNotFoundException ex) {
      finishPending(errorMap("no_browser_available", "No suitable browser is available for OAuth."));
    }
  }

  private void onAuthTabResult(AuthTabIntent.AuthResult authResult) {
    if (pending == null) {
      return;
    }
    int code = authResult.resultCode;
    if (code == AuthTabIntent.RESULT_OK) {
      Uri resultUri = authResult.resultUri;
      if (resultUri == null) {
        finishPending(errorMap("missing_authorization_code", "Auth Tab returned no redirect URI."));
        return;
      }
      finishPending(responseFromRedirectUri(pending.request, resultUri));
      return;
    }
    if (code == AuthTabIntent.RESULT_CANCELED) {
      finishPending(errorMap("cancelled", "User cancelled authorization."));
      return;
    }
    finishPending(
        errorMap(
            "authorize_failed",
            "Auth Tab failed with result code " + code + "."));
  }

  @Override
  public boolean onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
    if (requestCode != RC_EXTERNAL_BROWSER_AUTH || pending == null) {
      return false;
    }
    if (data == null) {
      finishPending(errorMap("cancelled", "User cancelled authorization."));
      return true;
    }
    AuthorizationResponse response = AuthorizationResponse.fromIntent(data);
    AuthorizationException ex = AuthorizationException.fromIntent(data);
    if (ex != null) {
      String message = ex.errorDescription != null ? ex.errorDescription : ex.error;
      if (message == null) {
        message = "Authorization failed.";
      }
      boolean cancelled =
          AuthorizationException.GeneralErrors.USER_CANCELED_AUTH_FLOW.equals(ex)
              || AuthorizationException.GeneralErrors.PROGRAM_CANCELED_AUTH_FLOW.equals(ex)
              || (ex.error != null && ex.error.toLowerCase().contains("cancel"));
      String error = cancelled ? "cancelled" : (ex.error != null ? ex.error : "authorize_failed");
      finishPending(errorMap(error, message));
      return true;
    }
    if (response == null || response.authorizationCode == null || response.authorizationCode.isEmpty()) {
      finishPending(errorMap("missing_authorization_code", "Authorization completed without a code."));
      return true;
    }
    Map<String, Object> map = new HashMap<>();
    map.put("authorization_code", response.authorizationCode);
    map.put("code_verifier", pending.request.codeVerifier);
    finishPending(map);
    return true;
  }

  private Map<String, Object> responseFromRedirectUri(AuthorizationRequest request, Uri resultUri) {
    String error = resultUri.getQueryParameter("error");
    if (error != null && !error.isEmpty()) {
      String description = resultUri.getQueryParameter("error_description");
      return errorMap(error, description != null ? description : error);
    }
    String code = resultUri.getQueryParameter("code");
    if (code == null || code.isEmpty()) {
      return errorMap("missing_authorization_code", "Redirect URI contained no authorization code.");
    }
    String state = resultUri.getQueryParameter("state");
    if (request.state != null && state != null && !request.state.equals(state)) {
      return errorMap("invalid_state", "OAuth state mismatch in Auth Tab redirect.");
    }
    Map<String, Object> map = new HashMap<>();
    map.put("authorization_code", code);
    map.put("code_verifier", request.codeVerifier);
    return map;
  }

  @SuppressWarnings("unchecked")
  private AuthorizationRequest buildAuthorizationRequest(Map<String, Object> args) {
    String clientId = requireString(args, "client_id");
    String redirectUrl = requireString(args, "redirect_url");
    String authorizationEndpoint = requireString(args, "authorization_endpoint");
    String tokenEndpoint = requireString(args, "token_endpoint");

    AuthorizationServiceConfiguration serviceConfiguration =
        new AuthorizationServiceConfiguration(
            Uri.parse(authorizationEndpoint), Uri.parse(tokenEndpoint));

    AuthorizationRequest.Builder builder =
        new AuthorizationRequest.Builder(
            serviceConfiguration, clientId, ResponseTypeValues.CODE, Uri.parse(redirectUrl));

    Object scopesObj = args.get("scopes");
    if (scopesObj instanceof List) {
      ArrayList<String> scopes = new ArrayList<>();
      for (Object scope : (List<?>) scopesObj) {
        if (scope != null) {
          scopes.add(scope.toString());
        }
      }
      if (!scopes.isEmpty()) {
        builder.setScopes(scopes);
      }
    }

    Object additionalObj = args.get("additional_parameters");
    if (additionalObj instanceof Map) {
      Map<String, String> additional = new HashMap<>();
      for (Map.Entry<?, ?> entry : ((Map<?, ?>) additionalObj).entrySet()) {
        if (entry.getKey() != null && entry.getValue() != null) {
          additional.put(entry.getKey().toString(), entry.getValue().toString());
        }
      }
      // AppAuth-Android forbids built-in OAuth fields in additionalParameters
      // (prompt, login_hint, …). max_age is NOT built-in in 0.11.1 — leave it.
      String prompt = additional.remove("prompt");
      if (prompt != null && !prompt.isEmpty()) {
        builder.setPrompt(prompt);
      }
      String loginHint = additional.remove("login_hint");
      if (loginHint != null && !loginHint.isEmpty()) {
        builder.setLoginHint(loginHint);
      }
      if (!additional.isEmpty()) {
        builder.setAdditionalParameters(additional);
      }
    }

    return builder.build();
  }

  private static String requireString(Map<String, Object> args, String key) {
    Object value = args.get(key);
    if (!(value instanceof String) || ((String) value).isEmpty()) {
      throw new IllegalArgumentException("Missing authorize argument: " + key);
    }
    return (String) value;
  }

  private void finishPending(Map<String, Object> payload) {
    PendingAuthorize current = pending;
    pending = null;
    disposeExternalBrowserService();
    if (current != null) {
      current.result.success(payload);
    }
  }

  private void disposeExternalBrowserService() {
    if (externalBrowserAuthService != null) {
      externalBrowserAuthService.dispose();
      externalBrowserAuthService = null;
    }
  }

  private static Map<String, Object> errorMap(String error, String description) {
    Map<String, Object> map = new HashMap<>();
    map.put("error", error);
    map.put("error_description", description);
    return map;
  }

  private static final class PendingAuthorize {
    final AuthorizationRequest request;
    final Result result;

    PendingAuthorize(AuthorizationRequest request, Result result) {
      this.request = request;
      this.result = result;
    }
  }
}
