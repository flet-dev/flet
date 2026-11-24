package dev.flet.flet_notifications;

import androidx.annotation.NonNull;

import io.flutter.embedding.engine.plugins.FlutterPlugin;

/**
 * Has no behavior of its own: it makes the package an Android plugin, so its
 * manifest is merged into the app's.
 */
public class FletNotificationsPlugin implements FlutterPlugin {
    @Override
    public void onAttachedToEngine(@NonNull FlutterPluginBinding binding) {}

    @Override
    public void onDetachedFromEngine(@NonNull FlutterPluginBinding binding) {}
}
