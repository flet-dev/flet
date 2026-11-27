package dev.flet.flet;

import androidx.annotation.NonNull;

import io.flutter.embedding.engine.plugins.FlutterPlugin;
import io.flutter.embedding.engine.plugins.activity.ActivityAware;
import io.flutter.embedding.engine.plugins.activity.ActivityPluginBinding;

/**
 * Root Flutter plugin for {@code packages/flet} native Android features.
 */
public class FletPlugin implements FlutterPlugin, ActivityAware {
  private FletWebAuthPlugin webAuthPlugin;

  @Override
  public void onAttachedToEngine(@NonNull FlutterPluginBinding binding) {
    webAuthPlugin = new FletWebAuthPlugin();
    webAuthPlugin.onAttachedToEngine(binding);
  }

  @Override
  public void onDetachedFromEngine(@NonNull FlutterPluginBinding binding) {
    if (webAuthPlugin != null) {
      webAuthPlugin.onDetachedFromEngine(binding);
      webAuthPlugin = null;
    }
  }

  @Override
  public void onAttachedToActivity(@NonNull ActivityPluginBinding binding) {
    if (webAuthPlugin != null) {
      webAuthPlugin.onAttachedToActivity(binding);
    }
  }

  @Override
  public void onDetachedFromActivityForConfigChanges() {
    if (webAuthPlugin != null) {
      webAuthPlugin.onDetachedFromActivityForConfigChanges();
    }
  }

  @Override
  public void onReattachedToActivityForConfigChanges(@NonNull ActivityPluginBinding binding) {
    if (webAuthPlugin != null) {
      webAuthPlugin.onReattachedToActivityForConfigChanges(binding);
    }
  }

  @Override
  public void onDetachedFromActivity() {
    if (webAuthPlugin != null) {
      webAuthPlugin.onDetachedFromActivity();
    }
  }
}
