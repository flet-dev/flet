#include "my_application.h"

#include <errno.h>
#include <fcntl.h>
#include <flutter_linux/flutter_linux.h>
#include <glib-unix.h>
#include <glib/gstdio.h>
#include <signal.h>
#include <string.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <unistd.h>
#ifdef GDK_WINDOWING_X11
#include <gdk/gdkx.h>
#endif

#include "flutter/generated_plugin_registrant.h"

struct _MyApplication {
  GtkApplication parent_instance;
  char** dart_entrypoint_arguments;
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

// Marks a desktop entry this app installed for itself, so it is only ever
// rewritten or removed when it is the app's own.
#define FLET_GENERATED_KEY "X-Flet-Generated"

// While the app runs with its desktop entry installed: the entry, the
// directory holding the app's runtime files, and this instance's marker in it.
static gchar* installed_entry = nullptr;
static gchar* runtime_dir = nullptr;
static gchar* instance_marker = nullptr;

// Who a desktop entry in the user's data directory belongs to.
typedef enum { ENTRY_ABSENT, ENTRY_OWN, ENTRY_FOREIGN } EntryOwner;

// Serializes entry updates and the last instance's cleanup. Keep the lock
// beside the runtime directory, and never unlink it: replacing its inode
// would let a new instance bypass a lock another instance still holds.
class DesktopEntryLock {
 public:
  explicit DesktopEntryLock(const gchar* dir) {
    g_autofree gchar* parent = g_path_get_dirname(dir);
    if (g_mkdir_with_parents(parent, 0700) != 0) {
      return;
    }
    g_autofree gchar* path = g_strconcat(dir, ".lock", nullptr);
    fd_ = g_open(path, O_CREAT | O_RDWR | O_CLOEXEC, 0600);
    if (fd_ < 0) {
      return;
    }
    while (flock(fd_, LOCK_EX) != 0) {
      if (errno != EINTR) {
        close(fd_);
        fd_ = -1;
        return;
      }
    }
  }

  ~DesktopEntryLock() {
    if (fd_ >= 0) {
      close(fd_);
    }
  }

  bool acquired() const { return fd_ >= 0; }

 private:
  int fd_ = -1;
};

// Tells whose entry is at `path`, and returns an own entry's `contents`.
//
// Only a regular file this app can read and that carries FLET_GENERATED_KEY
// is its own. Anything else that is there, such as an unreadable file or a
// symlink, is the user's, and must not be replaced.
static EntryOwner user_entry_owner(const gchar* path, gchar** contents) {
  GStatBuf status;
  if (g_lstat(path, &status) != 0) {
    return errno == ENOENT ? ENTRY_ABSENT : ENTRY_FOREIGN;
  }
  g_autofree gchar* data = nullptr;
  g_autoptr(GKeyFile) entry = g_key_file_new();
  if (!S_ISREG(status.st_mode) ||
      !g_file_get_contents(path, &data, nullptr, nullptr) ||
      !g_key_file_load_from_data(entry, data, -1, G_KEY_FILE_NONE, nullptr) ||
      !g_key_file_has_key(entry, G_KEY_FILE_DESKTOP_GROUP, FLET_GENERATED_KEY,
                          nullptr)) {
    return ENTRY_FOREIGN;
  }
  if (contents != nullptr) {
    *contents = g_steal_pointer(&data);
  }
  return ENTRY_OWN;
}

// Returns whether `a` and `b` are the same file.
static gboolean same_file(const gchar* a, const gchar* b) {
  GStatBuf a_status, b_status;
  return g_stat(a, &a_status) == 0 && g_stat(b, &b_status) == 0 &&
         a_status.st_dev == b_status.st_dev &&
         a_status.st_ino == b_status.st_ino;
}

// Returns whether another instance of the app runs, going by the markers in
// `dir`; markers of instances that have exited are removed.
static gboolean other_instance_running(const gchar* dir) {
  g_autoptr(GDir) markers = g_dir_open(dir, 0, nullptr);
  if (markers == nullptr) {
    return FALSE;
  }
  gboolean running = FALSE;
  const gchar* name;
  while ((name = g_dir_read_name(markers)) != nullptr) {
    gchar* end = nullptr;
    gint64 pid = g_ascii_strtoll(name, &end, 10);
    if (end == name || *end != '\0' || pid <= 0 || pid == getpid()) {
      continue;
    }
    if (kill((pid_t)pid, 0) == 0 || errno == EPERM) {
      running = TRUE;
    } else {
      g_autofree gchar* marker = g_build_filename(dir, name, nullptr);
      g_remove(marker);
    }
  }
  return running;
}

// Quotes `path` as one argument of a desktop entry's Exec key: inside double
// quotes, `"`, `` ` ``, `$` and `\` are backslash-escaped.
static gchar* quote_exec_argument(const gchar* path) {
  GString* quoted = g_string_new("\"");
  for (const gchar* c = path; *c != '\0'; c++) {
    if (*c == '"' || *c == '`' || *c == '$' || *c == '\\') {
      g_string_append_c(quoted, '\\');
    }
    g_string_append_c(quoted, *c);
  }
  g_string_append_c(quoted, '"');
  return g_string_free(quoted, FALSE);
}

// Removes the desktop entry install_desktop_entry() installed, once no other
// instance of the app runs.
static void remove_desktop_entry() {
  if (instance_marker == nullptr) {
    return;
  }
  DesktopEntryLock lock(runtime_dir);
  if (!lock.acquired()) {
    return;
  }
  g_remove(instance_marker);
  if (!other_instance_running(runtime_dir)) {
    if (user_entry_owner(installed_entry, nullptr) == ENTRY_OWN) {
      g_remove(installed_entry);
    }
    g_autofree gchar* icon = g_build_filename(runtime_dir, "icon.png", nullptr);
    g_remove(icon);
    g_rmdir(runtime_dir);
  }
  g_clear_pointer(&instance_marker, g_free);
  g_clear_pointer(&installed_entry, g_free);
  g_clear_pointer(&runtime_dir, g_free);
}

// Removes the desktop entry when the app is told to terminate, as at logout,
// then terminates as the signal would have.
static gboolean on_terminate_signal(gpointer signal_number) {
  remove_desktop_entry();
  signal(GPOINTER_TO_INT(signal_number), SIG_DFL);
  raise(GPOINTER_TO_INT(signal_number));
  return G_SOURCE_REMOVE;
}

// Installs the bundle's desktop entry for the current user while the app
// runs, so desktops that take an app's icon and name only from an installed
// entry show them.
//
// GNOME Shell does that on Wayland, and from version 46 on X11 too, and so do
// KDE Plasma and COSMIC on Wayland: without an entry the dock shows a generic
// icon and the app id as its name. The entry must be named after the app id,
// as the desktop finds it by that name. It is hidden from the application
// launcher (`NoDisplay`), and points at this executable, or at the AppImage
// the app runs from, and at a copy of the bundle's icon that stays put while
// any instance runs.
//
// The last instance to exit removes it, so it never outlives the app: an
// entry in the user's directory takes precedence over a package's, and would
// hide a version of the app installed later from the launcher.
//
// An entry the user installed is left alone, and so are sandboxed apps, which
// Flatpak and Snap register, and an app a package installed with its own entry.
static void install_desktop_entry(const gchar* exe_path) {
  if (g_getenv("FLATPAK_ID") != nullptr || g_getenv("SNAP") != nullptr) {
    return;
  }
  // An AppImage runs from a mount that goes away with it.
  const gchar* launch_path = g_getenv("APPIMAGE");
  const gboolean is_appimage = launch_path != nullptr && *launch_path != '\0';
  if (!is_appimage) {
    launch_path = exe_path;
  }
  // GLib checks that an entry's program exists using the path as written,
  // but expands `%` codes in it to launch it, so no Exec works for a path
  // with a `%`.
  if (strchr(launch_path, '%') != nullptr) {
    return;
  }

  g_autofree gchar* app_runtime_dir = g_build_filename(
      g_get_user_runtime_dir(), "flet", APPLICATION_ID, nullptr);
  DesktopEntryLock lock(app_runtime_dir);
  if (!lock.acquired()) {
    return;
  }

  g_autofree gchar* entry_name = g_strconcat(APPLICATION_ID, ".desktop", nullptr);
  g_autofree gchar* user_entry = g_build_filename(
      g_get_user_data_dir(), "applications", entry_name, nullptr);
  g_autofree gchar* installed = nullptr;
  EntryOwner owner = user_entry_owner(user_entry, &installed);
  if (owner == ENTRY_FOREIGN) {
    return;
  }

  // The bundle keeps its entry in `share/` next to the executable; an AppImage
  // or another `prefix/bin` + `prefix/share` layout keeps it a level up.
  g_autofree gchar* exe_dir = g_path_get_dirname(exe_path);
  g_autofree gchar* source = g_build_filename(exe_dir, "share", "applications",
                                              entry_name, nullptr);
  g_autoptr(GKeyFile) entry = g_key_file_new();
  if (!g_key_file_load_from_file(entry, source, G_KEY_FILE_NONE, nullptr)) {
    g_free(source);
    source = g_build_filename(exe_dir, "..", "share", "applications",
                              entry_name, nullptr);
    if (!g_key_file_load_from_file(entry, source, G_KEY_FILE_NONE, nullptr)) {
      return;
    }
  }

  // A prefix/bin + prefix/share install can use the source itself as its
  // system entry. Preserve it too; same_file() alone cannot distinguish an
  // installed entry from a wrapper's process-local XDG_DATA_DIRS addition.
  // Only an AppImage's own entry is known to live on a temporary mount.
  for (const gchar* const* dir = g_get_system_data_dirs(); *dir != nullptr;
       dir++) {
    g_autofree gchar* system_entry =
        g_build_filename(*dir, "applications", entry_name, nullptr);
    if (g_file_test(system_entry, G_FILE_TEST_EXISTS) &&
        !(is_appimage && same_file(system_entry, source))) {
      if (owner == ENTRY_OWN) {
        g_remove(user_entry);
      }
      return;
    }
  }

  // The lock keeps cleanup from removing the entry between the ownership
  // check above and this instance publishing its marker and entry.
  g_autofree gchar* pid = g_strdup_printf("%d", (int)getpid());
  g_autofree gchar* marker = g_build_filename(app_runtime_dir, pid, nullptr);
  if (g_mkdir_with_parents(app_runtime_dir, 0700) != 0 ||
      !g_file_set_contents(marker, "", 0, nullptr)) {
    return;
  }

  g_autofree gchar* exec_path = quote_exec_argument(launch_path);
  g_autofree gchar* exec = g_strconcat(exec_path, " %U", nullptr);
  g_key_file_set_string(entry, G_KEY_FILE_DESKTOP_GROUP,
                        G_KEY_FILE_DESKTOP_KEY_EXEC, exec);
  g_autofree gchar* bundle_icon =
      g_build_filename(exe_dir, "data", "app_icon.png", nullptr);
  g_autofree gchar* icon_data = nullptr;
  gsize icon_size = 0;
  if (g_file_get_contents(bundle_icon, &icon_data, &icon_size, nullptr)) {
    g_autofree gchar* icon =
        g_build_filename(app_runtime_dir, "icon.png", nullptr);
    g_key_file_set_string(
        entry, G_KEY_FILE_DESKTOP_GROUP, G_KEY_FILE_DESKTOP_KEY_ICON,
        g_file_set_contents(icon, icon_data, icon_size, nullptr) ? icon
                                                                 : bundle_icon);
  }
  g_key_file_set_boolean(entry, G_KEY_FILE_DESKTOP_GROUP,
                         G_KEY_FILE_DESKTOP_KEY_NO_DISPLAY, TRUE);
  g_key_file_set_boolean(entry, G_KEY_FILE_DESKTOP_GROUP, FLET_GENERATED_KEY,
                         TRUE);
  // The bundle's comment explains installing the entry by hand.
  g_key_file_remove_comment(entry, nullptr, nullptr, nullptr);

  g_autofree gchar* contents = g_key_file_to_data(entry, nullptr, nullptr);
  if (g_strcmp0(contents, installed) != 0) {
    g_autofree gchar* user_dir = g_path_get_dirname(user_entry);
    g_autoptr(GError) error = nullptr;
    if (g_mkdir_with_parents(user_dir, 0700) != 0 ||
        !g_file_set_contents(user_entry, contents, -1, &error)) {
      g_warning("Failed to install desktop entry %s: %s", user_entry,
                error != nullptr ? error->message : g_strerror(errno));
      g_remove(marker);
      return;
    }
  }

  installed_entry = g_steal_pointer(&user_entry);
  runtime_dir = g_steal_pointer(&app_runtime_dir);
  instance_marker = g_steal_pointer(&marker);
  // Closing the window runs the app's shutdown, which removes the entry;
  // `sys.exit()` ends the process at once, leaving it to the next start.
  atexit(remove_desktop_entry);
  const int terminate_signals[] = {SIGTERM, SIGINT, SIGHUP};
  for (int signal_number : terminate_signals) {
    g_unix_signal_add(signal_number, on_terminate_signal,
                      GINT_TO_POINTER(signal_number));
  }
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
    gtk_header_bar_set_title(header_bar, "{{ cookiecutter.product_name }}");
    gtk_header_bar_set_show_close_button(header_bar, TRUE);
    gtk_window_set_titlebar(window, GTK_WIDGET(header_bar));
  } else {
    gtk_window_set_title(window, "{{ cookiecutter.product_name }}");
  }

  // Use the bundled app icon as the default window icon. On X11 (and
  // XWayland) it is exported as the _NET_WM_ICON property read by taskbars
  // and window switchers. Native Wayland sessions have no window-icon
  // protocol GTK 3 can use; there the desktop environment resolves the icon
  // from an installed APPLICATION_ID.desktop entry instead, which
  // install_desktop_entry() provides.
  g_autofree gchar* exe_path = g_file_read_link("/proc/self/exe", nullptr);
  if (exe_path != nullptr) {
    // `[tool.flet.linux].desktop_entry=false` turns the entry off.
    if ({{ "FALSE" if get_pyproject("tool.flet.linux.desktop_entry") == false else "TRUE" }}) {
      install_desktop_entry(exe_path);
    }
    g_autofree gchar* exe_dir = g_path_get_dirname(exe_path);
    g_autofree gchar* icon_path =
        g_build_filename(exe_dir, "data", "app_icon.png", nullptr);
    g_autoptr(GError) icon_error = nullptr;
    g_autoptr(GdkPixbuf) icon = gdk_pixbuf_new_from_file(icon_path, &icon_error);
    if (icon == nullptr) {
      // A bundle may legitimately ship without an icon (a plain
      // `flutter build`, or a custom build template that has none), so only
      // an icon that is present but will not decode is worth a warning.
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
        gint scaled_width =
            MAX(1, (gint)((gint64)width * 256 / largest_side));
        gint scaled_height =
            MAX(1, (gint)((gint64)height * 256 / largest_side));
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

  gtk_widget_realize(GTK_WIDGET(window));

  g_autoptr(FlDartProject) project = fl_dart_project_new();
  fl_dart_project_set_dart_entrypoint_arguments(project, self->dart_entrypoint_arguments);
  // `flet build --no-impeller` renders with Skia; FLET_NO_IMPELLER does the
  // same when the app starts.
  if ({{ "FALSE" if cookiecutter.options.impeller else "TRUE" }} || no_impeller_requested()) {
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
  remove_desktop_entry();

  G_APPLICATION_CLASS(my_application_parent_class)->shutdown(application);
}

// Implements GObject::dispose.
static void my_application_dispose(GObject* object) {
  MyApplication* self = MY_APPLICATION(object);
  g_clear_pointer(&self->dart_entrypoint_arguments, g_strfreev);
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
