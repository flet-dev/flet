#include "my_application.h"

#include <flutter_linux/flutter_linux.h>
#include <string.h>
#ifdef GDK_WINDOWING_X11
#include <gdk/gdkx.h>
#endif

#include "flutter/generated_plugin_registrant.h"

struct _MyApplication {
  GtkApplication parent_instance;
  char** dart_entrypoint_arguments;
  GtkWindow* window;
  // Applies `page.window` size limits; see window_method_call_cb().
  FlMethodChannel* window_channel;
  // The size limits the app set, in content size, and which of them are set.
  GdkGeometry size_limits;
  GdkWindowHints size_limit_hints;
  // The decoration size last added to `size_limits` for GTK.
  gint applied_decoration_width;
  gint applied_decoration_height;
};

G_DEFINE_TYPE(MyApplication, my_application, GTK_TYPE_APPLICATION)

// Returns TRUE when the app should render with Skia instead of Flutter's
// default, Impeller: FLET_NO_IMPELLER is "1", "true" or "yes" (any case), or
// FLUTTER_LINUX_RENDERER picks the software renderer, which can't draw
// Impeller's text.
static gboolean no_impeller_requested() {
  const gchar* no_impeller = g_getenv("FLET_NO_IMPELLER");
  if (no_impeller != nullptr && (g_strcmp0(no_impeller, "1") == 0 ||
                                 g_ascii_strcasecmp(no_impeller, "true") == 0 ||
                                 g_ascii_strcasecmp(no_impeller, "yes") == 0)) {
    return TRUE;
  }
  return g_strcmp0(g_getenv("FLUTTER_LINUX_RENDERER"), "software") == 0;
}

// Maximum width or height of a window without a maximum on that axis. GDK
// multiplies hints by the display scale for X11, so G_MAXINT would overflow
// there and leave a 1 px limit.
#define NO_MAX_WINDOW_SIZE G_MAXSHORT

// Returns how much larger the window is than its content: the header bar and
// shadow GTK draws around a window with client-side decorations, or nothing.
// Only known once the window is shown.
static void get_decoration_size(GtkWindow* window, gint* width, gint* height) {
  *width = 0;
  *height = 0;
  GdkWindow* gdk_window = gtk_widget_get_window(GTK_WIDGET(window));
  if (gdk_window == nullptr || !gtk_widget_get_mapped(GTK_WIDGET(window))) {
    return;
  }
  gint content_width, content_height;
  gtk_window_get_size(window, &content_width, &content_height);
  *width = MAX(0, gdk_window_get_width(gdk_window) - content_width);
  *height = MAX(0, gdk_window_get_height(gdk_window) - content_height);
}

// Hands the app's size limits to GTK.
//
// GTK reads geometry hints in window size, decorations included, while
// `page.window.width`/`height` and the limits are content size, so the
// decoration size is added to them. Hints go through GtkWindow, which would
// replace any set directly on its GdkWindow the next time it computes its own.
static void apply_size_limits(MyApplication* self) {
  if (self->window == nullptr) {
    return;
  }
  gint decoration_width, decoration_height;
  get_decoration_size(self->window, &decoration_width, &decoration_height);
  GdkGeometry geometry = self->size_limits;
  if (self->size_limit_hints & GDK_HINT_MIN_SIZE) {
    geometry.min_width += decoration_width;
    geometry.min_height += decoration_height;
  }
  if (self->size_limit_hints & GDK_HINT_MAX_SIZE) {
    geometry.max_width += decoration_width;
    geometry.max_height += decoration_height;
  }
  self->applied_decoration_width = decoration_width;
  self->applied_decoration_height = decoration_height;
  gtk_window_set_geometry_hints(self->window, nullptr, &geometry,
                                self->size_limit_hints);
}

// Re-applies the size limits when the decoration size changes: when the
// window is first shown, its title bar is hidden or shown, or it is
// maximized, tiled or restored.
static void on_window_size_allocate(GtkWidget* widget,
                                    GdkRectangle* allocation,
                                    gpointer user_data) {
  MyApplication* self = MY_APPLICATION(user_data);
  if (!(self->size_limit_hints & (GDK_HINT_MIN_SIZE | GDK_HINT_MAX_SIZE))) {
    return;
  }
  gint decoration_width, decoration_height;
  get_decoration_size(GTK_WINDOW(widget), &decoration_width,
                      &decoration_height);
  if (decoration_width != self->applied_decoration_width ||
      decoration_height != self->applied_decoration_height) {
    apply_size_limits(self);
  }
}

// Reads the size `key` of a method call's arguments, or returns -1 when it is
// missing or null.
static gint get_size_arg(FlValue* args, const gchar* key) {
  FlValue* value = fl_value_get_type(args) == FL_VALUE_TYPE_MAP
                       ? fl_value_lookup_string(args, key)
                       : nullptr;
  if (value == nullptr) {
    return -1;
  }
  switch (fl_value_get_type(value)) {
    case FL_VALUE_TYPE_FLOAT:
      return (gint)CLAMP(fl_value_get_float(value), 0.0,
                         (gdouble)NO_MAX_WINDOW_SIZE);
    case FL_VALUE_TYPE_INT:
      return (gint)CLAMP(fl_value_get_int(value), 0,
                         (gint64)NO_MAX_WINDOW_SIZE);
    default:
      return -1;
  }
}

// Handles the "flet/window" channel, which sets the window's minimum and
// maximum content size. window_manager hands its limits to the GdkWindow,
// where GtkWindow replaces them, so they would not apply. A width or height
// that is null has no limit; both null clears the limit.
static void window_method_call_cb(FlMethodChannel* channel,
                                  FlMethodCall* method_call,
                                  gpointer user_data) {
  MyApplication* self = MY_APPLICATION(user_data);
  const gchar* method = fl_method_call_get_name(method_call);
  FlValue* args = fl_method_call_get_args(method_call);
  gboolean is_min = strcmp(method, "setMinimumSize") == 0;
  gboolean is_max = strcmp(method, "setMaximumSize") == 0;
  if (!is_min && !is_max) {
    fl_method_call_respond_not_implemented(method_call, nullptr);
    return;
  }

  gint width = get_size_arg(args, "width");
  gint height = get_size_arg(args, "height");
  GdkWindowHints hint = is_min ? GDK_HINT_MIN_SIZE : GDK_HINT_MAX_SIZE;
  if (width < 0 && height < 0) {
    self->size_limit_hints =
        static_cast<GdkWindowHints>(self->size_limit_hints & ~hint);
  } else {
    self->size_limit_hints =
        static_cast<GdkWindowHints>(self->size_limit_hints | hint);
  }
  if (is_min) {
    self->size_limits.min_width = MAX(width, 0);
    self->size_limits.min_height = MAX(height, 0);
  } else {
    self->size_limits.max_width = width < 0 ? NO_MAX_WINDOW_SIZE : width;
    self->size_limits.max_height = height < 0 ? NO_MAX_WINDOW_SIZE : height;
  }
  apply_size_limits(self);
  fl_method_call_respond_success(method_call, nullptr, nullptr);
}

// Implements GApplication::activate.
static void my_application_activate(GApplication* application) {
  MyApplication* self = MY_APPLICATION(application);
  GtkWindow* window =
      GTK_WINDOW(gtk_application_window_new(GTK_APPLICATION(application)));

  // Use a header bar when running in GNOME as this is the common style used
  // by applications and is the setup most users will be using (e.g. Ubuntu
  // desktop).
  // If running on X and not using GNOME then just use a traditional title bar
  // in case the window manager does more exotic layout, e.g. tiling.
  // If running on Wayland assume the header bar will work (may need changing
  // if future cases occur).
  gboolean use_header_bar = TRUE;
#ifdef GDK_WINDOWING_X11
  GdkScreen* screen = gtk_window_get_screen(window);
  if (GDK_IS_X11_SCREEN(screen)) {
    const gchar* wm_name = gdk_x11_screen_get_window_manager_name(screen);
    if (g_strcmp0(wm_name, "GNOME Shell") != 0) {
      use_header_bar = FALSE;
    }
  }
#endif
  if (use_header_bar) {
    GtkHeaderBar* header_bar = GTK_HEADER_BAR(gtk_header_bar_new());
    gtk_widget_show(GTK_WIDGET(header_bar));
    gtk_header_bar_set_title(header_bar, "flet");
    gtk_header_bar_set_show_close_button(header_bar, TRUE);
    gtk_window_set_titlebar(window, GTK_WIDGET(header_bar));
  } else {
    gtk_window_set_title(window, "flet");
  }

  // Use the bundled app icon as the default window icon. On X11 (and
  // XWayland) it is exported as the _NET_WM_ICON property read by taskbars
  // and window switchers. Native Wayland sessions have no window-icon
  // protocol GTK 3 can use; there the desktop environment resolves the icon
  // from an installed APPLICATION_ID.desktop entry instead.
  g_autofree gchar* exe_path = g_file_read_link("/proc/self/exe", nullptr);
  if (exe_path != nullptr) {
    g_autofree gchar* exe_dir = g_path_get_dirname(exe_path);
    g_autofree gchar* icon_path =
        g_build_filename(exe_dir, "data", "app_icon.png", nullptr);
    g_autoptr(GError) icon_error = nullptr;
    g_autoptr(GdkPixbuf) icon = gdk_pixbuf_new_from_file(icon_path, &icon_error);
    if (icon == nullptr) {
      // A plain `flutter build` of the client ships no icon, so only an icon
      // that is present but will not decode is worth a warning.
      if (g_error_matches(icon_error, G_FILE_ERROR, G_FILE_ERROR_NOENT)) {
        g_debug("No app icon at %s", icon_path);
      } else {
        g_warning("Failed to load app icon %s: %s", icon_path,
                  icon_error != nullptr ? icon_error->message : "unknown error");
      }
    } else {
      // _NET_WM_ICON is capped at 256 KiB of pixel data, and GDK silently
      // drops any icon that does not fit — anything from 512x512 up — which
      // would leave the window with no icon at all. Scale bigger icons down.
      gint width = gdk_pixbuf_get_width(icon);
      gint height = gdk_pixbuf_get_height(icon);
      gint largest_side = MAX(width, height);
      if (largest_side > 256) {
        // 64-bit intermediates: width * 256 overflows gint for very wide
        // images, and -O3 is free to do anything at all with that.
        gint scaled_width = MAX(1, (gint)((gint64)width * 256 / largest_side));
        gint scaled_height = MAX(1, (gint)((gint64)height * 256 / largest_side));
        g_autoptr(GdkPixbuf) scaled = gdk_pixbuf_scale_simple(
            icon, scaled_width, scaled_height, GDK_INTERP_BILINEAR);
        if (scaled != nullptr) {
          gtk_window_set_default_icon(scaled);
        } else {
          g_warning("Failed to scale app icon %s", icon_path);
        }
      } else {
        gtk_window_set_default_icon(icon);
      }
    }
  }

  gtk_window_set_default_size(window, 1280, 720);
  // A window can only be transparent if its surface carries an alpha channel,
  // which means selecting an RGBA visual. GTK only applies a visual before the
  // widget is realized, and without a compositor there is nothing to blend the
  // result against, so fall back to the default visual in that case.
  GdkScreen* rgba_screen = gtk_window_get_screen(window);
  GdkVisual* rgba_visual = gdk_screen_get_rgba_visual(rgba_screen);
  if (rgba_visual != nullptr && gdk_screen_is_composited(rgba_screen)) {
    gtk_widget_set_visual(GTK_WIDGET(window), rgba_visual);
  }

  // Realize the native window without showing it so Dart can decide when to
  // display and position the window.
  gtk_widget_realize(GTK_WIDGET(window));

  g_autoptr(FlDartProject) project = fl_dart_project_new();
  fl_dart_project_set_dart_entrypoint_arguments(project, self->dart_entrypoint_arguments);
  // `flet run --no-impeller` sets FLET_NO_IMPELLER.
  if (no_impeller_requested()) {
    fl_dart_project_set_enable_impeller(project, FALSE);
  }

  FlView* view = fl_view_new(project);

  // The Flutter view paints an opaque black background by default, which would
  // cover a transparent window no matter what the app asks for. A fully
  // transparent colour makes the embedder skip that paint entirely, so
  // whatever GTK draws below shows through. This alone changes nothing for a
  // normal app: the top-level keeps painting its own opaque background until
  // an app sets Window.bgcolor to a transparent colour, which window_manager
  // applies as a CSS rule on the top-level.
  //
  // The colour is built directly rather than parsed from "#00000000": GDK3
  // resolves "#" specs through pango_color_parse(), which rejects the 8-digit
  // form outright and leaves the GdkRGBA untouched. The embedder only skips
  // the paint for exactly (0, 0, 0, 0), so it has to be exact.
  GdkRGBA background_color = {0.0, 0.0, 0.0, 0.0};
  fl_view_set_background_color(view, &background_color);
  gtk_widget_show(GTK_WIDGET(view));
  gtk_container_add(GTK_CONTAINER(window), GTK_WIDGET(view));

  // Realize the Flutter view while the top-level window is still hidden; this
  // lets Flutter render its first frames and lets integration tests attach
  // before Dart decides whether the app window should be shown.
  gtk_widget_realize(GTK_WIDGET(view));

  fl_register_plugins(FL_PLUGIN_REGISTRY(view));

  self->window = window;
  g_object_add_weak_pointer(G_OBJECT(window),
                            reinterpret_cast<gpointer*>(&self->window));
  g_autoptr(FlStandardMethodCodec) codec = fl_standard_method_codec_new();
  self->window_channel = fl_method_channel_new(
      fl_engine_get_binary_messenger(fl_view_get_engine(view)), "flet/window",
      FL_METHOD_CODEC(codec));
  fl_method_channel_set_method_call_handler(
      self->window_channel, window_method_call_cb, self, nullptr);
  g_signal_connect(window, "size-allocate",
                   G_CALLBACK(on_window_size_allocate), self);

  gtk_widget_grab_focus(GTK_WIDGET(view));
}

// Implements GApplication::local_command_line.
static gboolean my_application_local_command_line(GApplication* application, gchar*** arguments, int* exit_status) {
  MyApplication* self = MY_APPLICATION(application);
  // Strip out the first argument as it is the binary name.
  self->dart_entrypoint_arguments = g_strdupv(*arguments + 1);

  g_autoptr(GError) error = nullptr;
  if (!g_application_register(application, nullptr, &error)) {
     g_warning("Failed to register: %s", error->message);
     *exit_status = 1;
     return TRUE;
  }

  g_application_activate(application);
  *exit_status = 0;

  return TRUE;
}

// Implements GApplication::startup.
static void my_application_startup(GApplication* application) {
  //MyApplication* self = MY_APPLICATION(object);

  // Perform any actions required at application startup.

  G_APPLICATION_CLASS(my_application_parent_class)->startup(application);
}

// Implements GApplication::shutdown.
static void my_application_shutdown(GApplication* application) {
  //MyApplication* self = MY_APPLICATION(object);

  // Perform any actions required at application shutdown.

  G_APPLICATION_CLASS(my_application_parent_class)->shutdown(application);
}

// Implements GObject::dispose.
static void my_application_dispose(GObject* object) {
  MyApplication* self = MY_APPLICATION(object);
  g_clear_pointer(&self->dart_entrypoint_arguments, g_strfreev);
  g_clear_object(&self->window_channel);
  if (self->window != nullptr) {
    g_object_remove_weak_pointer(G_OBJECT(self->window),
                                 reinterpret_cast<gpointer*>(&self->window));
    self->window = nullptr;
  }
  G_OBJECT_CLASS(my_application_parent_class)->dispose(object);
}

static void my_application_class_init(MyApplicationClass* klass) {
  G_APPLICATION_CLASS(klass)->activate = my_application_activate;
  G_APPLICATION_CLASS(klass)->local_command_line = my_application_local_command_line;
  G_APPLICATION_CLASS(klass)->startup = my_application_startup;
  G_APPLICATION_CLASS(klass)->shutdown = my_application_shutdown;
  G_OBJECT_CLASS(klass)->dispose = my_application_dispose;
}

static void my_application_init(MyApplication* self) {}

MyApplication* my_application_new() {
  // Set the program name to the application ID, which helps various systems
  // like GTK and desktop environments map this running application to its
  // corresponding .desktop file. This ensures better integration by allowing
  // the application to be recognized beyond its binary name.
  g_set_prgname(APPLICATION_ID);

  return MY_APPLICATION(g_object_new(my_application_get_type(),
                                     "application-id", APPLICATION_ID,
                                     "flags", G_APPLICATION_NON_UNIQUE,
                                     nullptr));
}
