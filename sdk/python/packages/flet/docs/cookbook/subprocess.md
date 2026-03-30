In this cookbook recipe, you'll learn how to run external system commands from your
Flet app using Python's built-in [`subprocess`](https://docs.python.org/3/library/subprocess.html) module.

This approach is useful when you need to interact with platform tools or system utilities
that are not exposed through Flet APIs.

/// admonition | Note
Running external commands is **not supported when your app runs in a browser**.
///

## Examples

### Launching another Android app

Sometimes your Flet app may need to open another Android application.
For example, you might want to open the **Settings** app so the user can adjust system or app settings.

On Android, this can be done using the [`am start`](https://developer.android.com/tools/adb#IntentSpec)
command, which launches activities from the Android shell.

The command requires the **component name** (`-n`) of the target activity in the form: `package.name/.ActivityName`.

For example, the Android Settings app uses:

```text
com.android.settings/.Settings
```

It is also recommended to pass the `--user` flag. Without it, the command may fail with an error such as:

```bash
Security exception: Permission Denial: startActivityAsUser asks to run as
user -2 but is calling from uid u0a164; this requires android.permission.INTERACT_ACROSS_USERS_FULL
```

This happens because Android may attempt to launch the activity for a different user
than the one your app runs under. Setting `--user 0` ensures the command runs for the primary user.

The full command therefore becomes:

```bash
am start -n com.android.settings/.Settings --user 0
```

And can be run from a Flet app like this:

```python
import subprocess
import flet as ft


def main(page: ft.Page):
    def open_settings(e):
        result = subprocess.run(
            ["am", "start", "-n", "com.android.settings/.Settings", "--user", "0"],
            shell=False, # default
            capture_output=True,
            text=True,
        )

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

    page.add(
        ft.SafeArea(
            content=ft.Button("Open Settings app", on_click=open_settings)
        )
    )


ft.run(main)
```

Running this app on an Android device, you should see the **Settings** app launch when the button is clicked.

#### Common Pitfall

When using `subprocess.run()`, be careful with the `shell` argument.

This will **not work correctly**:

```python
subprocess.run(
    ["am", "start", "-n", "com.android.settings/.Settings", "--user", "0"],
    shell=True
)
```

Because when `shell=True` is used, the command must be passed as a **single string**, not a list.

Correct usage:

```python
subprocess.run(
    "am start -n com.android.settings/.Settings --user 0",
    shell=True
)
```

However, when possible, prefer **`shell=False` with a list of arguments**,
as shown in the main example. This is generally safer and avoids shell parsing issues.
