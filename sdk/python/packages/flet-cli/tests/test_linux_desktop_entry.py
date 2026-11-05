"""Exercise the Linux runner's desktop-entry helpers without Flutter or GTK."""

import os
import select
import shlex
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

APP_ID = "org.flet.DesktopEntryTest"
RUNNER = (
    Path(__file__).resolve().parents[3]
    / "templates/build/{{cookiecutter.out_dir}}/linux/my_application.cc"
)


@pytest.fixture(scope="module")
def desktop_entry_probe(tmp_path_factory):
    """Compile the actual helpers, adding barriers for concurrent processes."""
    compiler = shutil.which("c++")
    pkg_config = shutil.which("pkg-config")
    if os.name != "posix" or compiler is None or pkg_config is None:
        pytest.skip("Requires a POSIX C++ compiler and GLib development files")
    flags = subprocess.run(
        [pkg_config, "--cflags", "--libs", "glib-2.0"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if flags.returncode:
        pytest.skip("Requires GLib development files")

    runner = RUNNER.read_text()
    includes = "\n".join(
        line
        for line in runner.split("#ifdef GDK_WINDOWING_X11", 1)[0].splitlines()
        if line.startswith("#include <") and "flutter_linux" not in line
    )
    helpers = runner.split("#define FLET_GENERATED_KEY", 1)[1].split(
        "// Implements GApplication::activate.", 1
    )[0]
    source = (
        includes
        + f'\n#define APPLICATION_ID "{APP_ID}"\n'
        + r"""
#include <stdio.h>
#include <stdlib.h>
static bool pause_read = false;
static bool pause_remove = false;

static void barrier(const char* event) {
  puts(event);
  fflush(stdout);
  if (getchar() == EOF) exit(2);
}

static gboolean load_source(GKeyFile* entry, const gchar* path,
                            GKeyFileFlags flags, GError** error) {
  gboolean loaded = g_key_file_load_from_file(entry, path, flags, error);
  if (loaded && pause_read) {
    pause_read = false;
    barrier("snapshot");
  }
  return loaded;
}

static int remove_file(const gchar* path) {
  if (pause_remove && g_str_has_suffix(path, ".desktop")) {
    pause_remove = false;
    barrier("removing");
  }
  return g_remove(path);
}
#define g_key_file_load_from_file load_source
#undef g_remove
#define g_remove remove_file
#define FLET_GENERATED_KEY"""
        + helpers
        + r"""
int main(int argc, char** argv) {
  pause_read = argc > 2 && strcmp(argv[2], "pause-read") == 0;
  pause_remove = argc > 2 && strcmp(argv[2], "pause-remove") == 0;
  install_desktop_entry(argv[1]);
  barrier("ready");
  puts("stopping");
  fflush(stdout);
  remove_desktop_entry();
  puts("stopped");
  fflush(stdout);
}
"""
    )
    directory = tmp_path_factory.mktemp("desktop-entry-probe")
    cpp = directory / "probe.cc"
    cpp.write_text(source)
    executable = directory / "probe"
    result = subprocess.run(
        [
            compiler,
            "-std=c++14",
            "-Wall",
            "-Werror",
            str(cpp),
            "-o",
            str(executable),
            *shlex.split(flags.stdout),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return executable


class Probe:
    """Control a runner instance through explicit startup/cleanup barriers."""

    def __init__(self, executable, app, mode):
        self.process = subprocess.Popen(
            [str(executable), str(app.exe), mode],
            env=app.env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=0,
        )

    def expect(self, event):
        assert select.select([self.process.stdout], [], [], 5)[0], event
        assert self.process.stdout.readline().decode().strip() == event

    def resume(self):
        self.process.stdin.write(b"\n")
        self.process.stdin.flush()

    def stop(self):
        self.resume()
        self.expect("stopping")
        self.expect("stopped")
        assert self.process.wait(timeout=5) == 0


@pytest.fixture
def app(tmp_path):
    """Use isolated XDG directories and a prefix/bin + prefix/share bundle."""
    prefix = tmp_path / "prefix"
    exe = prefix / "bin/app"
    exe.parent.mkdir(parents=True)
    exe.touch()
    source = prefix / f"share/applications/{APP_ID}.desktop"
    source.parent.mkdir(parents=True)
    source.write_text(
        "[Desktop Entry]\nType=Application\nName=Probe\nExec=app\nIcon=probe\n"
    )
    icon = exe.parent / "data/app_icon.png"
    icon.parent.mkdir()
    icon.write_bytes(b"icon")
    runtime = tmp_path / "runtime"
    runtime.mkdir(mode=0o700)
    env = os.environ.copy()
    for variable in ("APPIMAGE", "FLATPAK_ID", "SNAP"):
        env.pop(variable, None)
    env.update(
        XDG_DATA_HOME=str(tmp_path / "data"),
        XDG_DATA_DIRS=str(tmp_path / "system-share"),
        XDG_RUNTIME_DIR=str(runtime),
    )
    return SimpleNamespace(
        exe=exe,
        source=source,
        env=env,
        entry=tmp_path / f"data/applications/{APP_ID}.desktop",
        runtime=runtime / "flet" / APP_ID,
    )


@pytest.fixture
def start_probe(desktop_entry_probe, app):
    """Always reap children, including when a concurrency assertion fails."""
    probes = []

    def start(mode=""):
        probe = Probe(desktop_entry_probe, app, mode)
        probes.append(probe)
        return probe

    yield start
    for probe in probes:
        if probe.process.poll() is None:
            probe.process.kill()
        probe.process.communicate(timeout=5)


@pytest.mark.parametrize("stale_entry", [False, True])
def test_preserve_system_entry_when_it_is_the_source(app, start_probe, stale_entry):
    """A packaged bin/share layout must never acquire a hidden user override."""
    app.env["XDG_DATA_DIRS"] = str(app.source.parent.parent)
    original = app.source.read_bytes()
    if stale_entry:
        app.entry.parent.mkdir(parents=True)
        app.entry.write_text("[Desktop Entry]\nX-Flet-Generated=true\nNoDisplay=true\n")
    probe = start_probe()
    probe.expect("ready")
    assert not app.entry.exists()
    assert not app.runtime.exists()
    probe.stop()
    assert app.source.read_bytes() == original


def test_appimage_source_in_process_data_dirs_still_registers(app, start_probe):
    """An AppImage wrapper's own mounted entry is not a system installation."""
    app.env["APPIMAGE"] = str(app.exe.parent.parent / "app.AppImage")
    app.env["XDG_DATA_DIRS"] = str(app.source.parent.parent)
    probe = start_probe()
    probe.expect("ready")
    assert "NoDisplay=true" in app.entry.read_text()
    assert app.env["APPIMAGE"] in app.entry.read_text()
    probe.stop()
    assert not app.entry.exists()
    assert not app.runtime.exists()


def test_shutdown_waits_for_startup_to_publish_its_marker(app, start_probe):
    """Cleanup cannot delete an entry a new instance has already read."""
    first = start_probe()
    first.expect("ready")
    second = start_probe("pause-read")
    second.expect("snapshot")
    first.resume()
    first.expect("stopping")
    with pytest.raises(subprocess.TimeoutExpired):
        first.process.wait(timeout=0.2)
    second.resume()
    second.expect("ready")
    first.expect("stopped")
    assert first.process.wait(timeout=5) == 0
    assert app.entry.exists()
    assert (app.runtime / "icon.png").exists()
    second.stop()
    assert not app.entry.exists()
    assert not app.runtime.exists()


def test_startup_waits_for_last_instance_cleanup(app, start_probe):
    """A new entry cannot be published between the last-instance scan/unlink."""
    first = start_probe("pause-remove")
    first.expect("ready")
    first.resume()
    first.expect("stopping")
    first.expect("removing")
    second = start_probe()
    assert not select.select([second.process.stdout], [], [], 0.2)[0]
    first.resume()
    first.expect("stopped")
    assert first.process.wait(timeout=5) == 0
    second.expect("ready")
    assert app.entry.exists()
    assert (app.runtime / "icon.png").exists()
    second.stop()
    assert not app.entry.exists()
    assert not app.runtime.exists()
