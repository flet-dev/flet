# SKILLS.md — Building Apps with Flet

> **Framework:** [Flet](https://flet.dev) — Build multi-platform apps in Python
> **Docs:** [docs.flet.dev](https://docs.flet.dev/)
> **Source:** [github.com/flet-dev/flet](https://github.com/flet-dev/flet)
> **License:** Apache-2.0 | **Python:** ≥ 3.10

---

## Table of Contents

- [What is Flet](#what-is-flet)
- [Installation & Project Setup](#installation--project-setup)
- [App Structure & Entry Point](#app-structure--entry-point)
- [Running Your App](#running-your-app)
- [Controls (UI Widgets)](#controls-ui-widgets)
- [Layout System](#layout-system)
- [Services (Non-Visual)](#services-non-visual)
- [Navigation & Routing](#navigation--routing)
- [Theming & Colors](#theming--colors)
- [Custom Controls](#custom-controls)
- [Async Apps](#async-apps)
- [Assets & Resources](#assets--resources)
- [State & Storage](#state--storage)
- [Animations](#animations)
- [Extension Packages](#extension-packages)
- [Creating Custom Extensions](#creating-custom-extensions)
- [Publishing & Packaging](#publishing--packaging)
- [Server-Side Web (FastAPI)](#server-side-web-fastapi)
- [Platform Support Matrix](#platform-support-matrix)
- [CLI Reference](#cli-reference)
- [Recommended Project Structure](#recommended-project-structure)
- [Common Patterns & Tips](#common-patterns--tips)
- [Control Parameters Reference](#control-parameters-reference)
- [Links & Resources](#links--resources)

---

## What is Flet

Flet is a Python framework for building multi-platform apps (iOS, Android, Windows, Linux, macOS, Web) using a single codebase with zero frontend experience required. It renders UI via Flutter and provides 150+ built-in controls with Material and Cupertino design.

Key capabilities:
- **Single Python codebase** for desktop, mobile, and web
- **Hot reload** during development
- **150+ controls and services** — buttons, forms, charts, maps, video, etc.
- **Native packaging** via `flet build` for all platforms
- **WebAssembly** web apps (no server) or **FastAPI** server-side web apps
- **Extensible** — wrap any Flutter package as a Flet extension

---

## Installation & Project Setup

### Prerequisites

- Python ≥ 3.10
- macOS 12+, Windows 10+ (64-bit), or Linux (Debian 10+/Ubuntu 20.04+)

### Install with uv (recommended)

```bash
mkdir my-flet-app && cd my-flet-app
uv init --python='>=3.10'
uv venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv add 'flet[all]'
```

### Install with pip

```bash
mkdir my-flet-app && cd my-flet-app
python -m venv .venv
source .venv/bin/activate               # Windows: .venv\Scripts\activate
pip install 'flet[all]'
```

### Scaffold a New Project

```bash
flet create                # Creates minimal app template
# or with uv:
uv run flet create
```

This generates:

```
src/
    assets/
        icon.png
    main.py         # Your app entry point
storage/
    data/
    temp/
pyproject.toml
README.md
```

### Install Extras

```bash
# Full install (desktop + web + CLI)
pip install 'flet[all]'

# Selective installs
pip install 'flet[cli]'       # CLI tools only
pip install 'flet[web]'       # Web runtime only
pip install 'flet[desktop]'   # Desktop runtime only
```

---

## App Structure & Entry Point

Every Flet app has a `main()` function that receives a `Page` object — the top-level container for your UI:

```python
import flet as ft

def main(page: ft.Page):
    page.title = "My App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Text("Hello, Flet!", size=30, weight=ft.FontWeight.BOLD)
    )

ft.run(main)
```

**Key concepts:**
- `ft.run(main)` initializes the app and calls your `main()` function
- `page` is the root — it holds all controls (views, dialogs, etc.)
- `page.add(...)` appends controls; `page.update()` pushes changes to the UI
- Controls auto-update when added via `page.add()`, but if you modify a control's properties afterward, call `page.update()` or `control.update()`

---

## Running Your App

```bash
# Desktop app (default: runs main.py in current directory)
flet run
flet run my_app.py                # Specific file

# Web app
flet run --web
flet run --web --port 8550        # Fixed port

# With uv
uv run flet run
uv run flet run --web -p 8550
```

Hot reload is enabled by default — save your file and the app refreshes.

---

## Controls (UI Widgets)

Flet provides 150+ controls. All controls are Python dataclasses accessed via `ft.<ControlName>`.

### Common Controls

| Category         | Controls                                                                                     |
| ---------------- | -------------------------------------------------------------------------------------------- |
| **Text**         | `Text`, `Markdown`, `Icon`                                                                   |
| **Input**        | `TextField`, `Dropdown`, `Checkbox`, `Radio`, `Switch`, `Slider`, `DatePicker`, `TimePicker`  |
| **Buttons**      | `Button`, `IconButton`, `FloatingActionButton`, `FilledButton`, `OutlinedButton`, `TextButton` |
| **Layout**       | `Row`, `Column`, `Stack`, `Container`, `Card`, `GridView`, `ListView`, `ResponsiveRow`        |
| **Navigation**   | `AppBar`, `NavigationBar`, `NavigationRail`, `NavigationDrawer`, `Tabs`                       |
| **Dialogs**      | `AlertDialog`, `BottomSheet`, `SnackBar`, `Banner`                                           |
| **Data Display** | `DataTable`, `DataTable2`, `ListTile`, `ExpansionTile`, `ExpansionPanel`                     |
| **Media**        | `Image`, `Video`, `Lottie`, `Rive`, `Canvas`                                                |
| **Charts**       | `BarChart`, `LineChart`, `PieChart`, `ScatterChart`, `RadarChart`, `CandlestickChart`        |
| **Cupertino**    | `CupertinoButton`, `CupertinoTextField`, `CupertinoAlertDialog`, `CupertinoSlider`, etc.    |

### Control Properties Pattern

Every control has properties you set declaratively:

```python
ft.TextField(
    label="Username",
    hint_text="Enter your name",
    width=300,
    on_change=lambda e: print(e.data),    # Event handler
)
```

### Event Handling

Events use callback functions — either sync or async:

```python
def button_clicked(e):
    page.add(ft.Text(f"Clicked! Data: {e.data}"))

ft.Button("Click me", on_click=button_clicked)
```

---

## Layout System

### Row & Column

```python
# Horizontal layout
ft.Row(controls=[ft.Text("A"), ft.Text("B"), ft.Text("C")])

# Vertical layout
ft.Column(controls=[ft.Text("1"), ft.Text("2"), ft.Text("3")])
```

### Expanding Controls

Use `expand` to fill available space:

```python
ft.Row([
    ft.TextField(hint_text="Search", expand=True),    # Takes remaining space
    ft.Button("Go"),                                   # Fixed size
])

# Proportional: 20% / 60% / 20%
ft.Row([
    ft.Container(expand=1, content=ft.Text("Left")),
    ft.Container(expand=3, content=ft.Text("Center")),
    ft.Container(expand=1, content=ft.Text("Right")),
])
```

### Container (Styling Wrapper)

```python
ft.Container(
    content=ft.Text("Styled"),
    width=200,
    height=100,
    bgcolor=ft.Colors.BLUE_100,
    border_radius=10,
    padding=20,
    alignment=ft.alignment.center,
)
```

### Responsive Layout

```python
ft.ResponsiveRow([
    ft.Container(ft.Text("A"), col={"sm": 12, "md": 6, "lg": 4}),
    ft.Container(ft.Text("B"), col={"sm": 12, "md": 6, "lg": 4}),
    ft.Container(ft.Text("C"), col={"sm": 12, "md": 12, "lg": 4}),
])
```

### Scrollable Content

```python
ft.Column(
    controls=[ft.Text(f"Item {i}") for i in range(100)],
    scroll=ft.ScrollType.AUTO,
    height=400,
)
```

---

## Services (Non-Visual)

Services provide platform features that are not UI controls:

| Service              | Usage                                                  |
| -------------------- | ------------------------------------------------------ |
| `FilePicker`         | File selection and upload                              |
| `Clipboard`          | Copy/paste text                                        |
| `Share`              | Native sharing dialog                                  |
| `UrlLauncher`        | Open URLs in browser                                   |
| `HapticFeedback`     | Vibration feedback                                     |
| `Audio`              | Audio playback                                         |
| `AudioRecorder`      | Audio recording                                        |
| `Geolocator`         | GPS/location services                                  |
| `Camera`             | Camera access                                          |
| `SecureStorage`      | Encrypted key-value storage                            |
| `SharedPreferences`  | Client-side persistent storage                         |
| `PermissionHandler`  | Runtime permission requests                            |
| `Connectivity`       | Network connectivity status                            |
| `Battery`            | Battery level and state                                |
| `Accelerometer`      | Motion sensors                                         |
| `Wakelock`           | Prevent screen sleep                                   |

Services are added to the page overlay or used via page properties:

```python
# File picker example
file_picker = ft.FilePicker(on_result=lambda e: print(e.files))
page.overlay.append(file_picker)
page.update()
file_picker.pick_files()

# Clipboard
await page.clipboard.set_data("Copied text")
text = await page.clipboard.get_data()
```

---

## Navigation & Routing

Flet supports multi-screen apps via route-based navigation:

```python
import flet as ft

def main(page: ft.Page):
    def route_change(e):
        page.views.clear()
        page.views.append(
            ft.View("/", [
                ft.AppBar(title=ft.Text("Home")),
                ft.Button("Go to Settings", on_click=lambda _: page.push_route("/settings")),
            ])
        )
        if page.route == "/settings":
            page.views.append(
                ft.View("/settings", [
                    ft.AppBar(title=ft.Text("Settings")),
                    ft.Text("Settings page"),
                ])
            )
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.push_route("/")

ft.run(main)
```

**Key routing concepts:**
- `page.route` — current route string (e.g., `/`, `/settings`)
- `page.views` — stack of `View` objects (navigation history)
- `page.push_route(route)` — navigate to a route (supports query params)
- `page.on_route_change` — rebuild views when route changes
- `page.on_view_pop` — handle Back navigation

---

## Theming & Colors

### App-Wide Theme

```python
page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
page.theme_mode = ft.ThemeMode.SYSTEM   # LIGHT, DARK, or SYSTEM
```

### Per-Container Theme Override

```python
ft.Container(
    theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.PINK)),
    content=ft.Button("Pink themed button"),
)

# Force dark mode in a section
ft.Container(
    theme=ft.Theme(color_scheme_seed=ft.Colors.INDIGO),
    theme_mode=ft.ThemeMode.DARK,
    content=ft.Button("Always dark"),
)
```

### Colors

```python
# Named colors (enum — preferred for autocompletion)
ft.Container(bgcolor=ft.Colors.BLUE_200)

# Hex colors
ft.Container(bgcolor="#ff5722")
ft.Container(bgcolor="#80ff5722")    # with alpha
```

### Theme Color Roles

Flet uses Material 3 dynamic color. Setting `color_scheme_seed` auto-generates 30 theme colors (primary, secondary, surface, error, etc.). Override individual colors via `ft.ColorScheme(...)`.

---

## Custom Controls

### Styled Control (Default Overrides)

```python
@ft.control
class PrimaryButton(ft.Button):
    bgcolor: ft.Colors = ft.Colors.BLUE_700
    color: ft.Colors = ft.Colors.WHITE
    style: ft.ButtonStyle = field(
        default_factory=lambda: ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        )
    )
```

### Composite Control (Combining Controls)

```python
@ft.control
class SearchBar(ft.Row):
    def init(self):
        self.controls = [
            ft.TextField(hint_text="Search...", expand=True),
            ft.IconButton(ft.Icons.SEARCH),
        ]
```

### Rules for Custom Controls

- Use `@ft.control` or `@dataclass` decorator on the inherited class
- Fields must have type annotations to override parent properties (e.g., `expand: int = 1`)
- Use `field(default_factory=lambda: ...)` for mutable defaults (classes, lists, dicts)
- Use `init()` method for initialization logic (not `__init__`)

---

## Async Apps

Flet natively supports async/await — essential for WASM web deployments:

```python
import asyncio
import flet as ft

async def main(page: ft.Page):
    async def on_click(e):
        await asyncio.sleep(1)
        page.add(ft.Text("Done!"))

    page.add(ft.Button("Start", on_click=on_click))

ft.run(main)
```

**Guidelines:**
- If `main()` is `async`, event handlers can be `async` too
- Use `asyncio.sleep()` instead of `time.sleep()` in async apps
- Sync handlers are fine alongside async `main()` if they don't call async code
- For WebAssembly (static web) deployment, async is required (Pyodide has no threading)

---

## Assets & Resources

Place assets in an `assets/` directory (default) relative to your entry file:

```
assets/
    images/
        logo.png
    fonts/
        custom.ttf
main.py
```

```python
# Reference assets by path relative to assets dir
ft.Image(src="images/logo.png")

# Configure assets directory
ft.run(main, assets_dir="assets")
```

---

## State & Storage

### Client Storage (SharedPreferences)

Persistent key-value storage on the client device:

```python
# Write
await page.shared_preferences.set("username", "john")
await page.shared_preferences.set("scores", [100, 200, 300])

# Read
name = await page.shared_preferences.get("username")

# Check / Delete
exists = await page.shared_preferences.contains_key("username")
await page.shared_preferences.remove("username")
```

### Secure Storage

For sensitive data (tokens, passwords):

```python
import flet as ft
from flet_secure_storage import SecureStorage

secure = SecureStorage()
page.overlay.append(secure)
page.update()

await secure.write("auth_token", "secret123")
token = await secure.read("auth_token")
```

### Session Storage

Per-session server-side storage (for server-side web apps):

```python
page.session.set("cart", [])
cart = page.session.get("cart")
```

---

## Animations

### Implicit Animations

Animate property changes automatically:

```python
c = ft.Container(
    width=100, height=100,
    bgcolor=ft.Colors.RED,
    animate=ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_OUT),
    animate_opacity=300,
    animate_rotation=ft.Animation(500, ft.AnimationCurve.BOUNCE_OUT),
)

# Changing properties triggers animation
c.width = 200
c.opacity = 0.5
c.rotate = ft.Rotate(angle=3.14)
page.update()
```

Animatable properties: `opacity`, `rotation`, `scale`, `offset`, `position`, and `Container` size/color.

### AnimatedSwitcher

Animate between different child controls:

```python
ft.AnimatedSwitcher(
    content=ft.Text("Hello"),
    transition=ft.AnimatedSwitcherTransition.SCALE,
    duration=500,
)
```

---

## Extension Packages

Install separately to add specialized capabilities:

| Package                  | Install                           | Purpose                   |
| ------------------------ | --------------------------------- | ------------------------- |
| `flet-ads`               | `pip install flet-ads`            | Google Mobile Ads         |
| `flet-audio`             | `pip install flet-audio`          | Audio playback            |
| `flet-audio-recorder`    | `pip install flet-audio-recorder` | Audio recording           |
| `flet-camera`            | `pip install flet-camera`         | Camera access             |
| `flet-charts`            | `pip install flet-charts`         | Chart widgets             |
| `flet-code-editor`       | `pip install flet-code-editor`    | Code editor control       |
| `flet-color-pickers`     | `pip install flet-color-pickers`  | Color picker controls     |
| `flet-datatable2`        | `pip install flet-datatable2`     | Advanced DataTable        |
| `flet-flashlight`        | `pip install flet-flashlight`     | Flashlight/torch          |
| `flet-geolocator`        | `pip install flet-geolocator`     | GPS/location services     |
| `flet-lottie`            | `pip install flet-lottie`         | Lottie animations         |
| `flet-map`               | `pip install flet-map`            | Interactive maps          |
| `flet-permission-handler`| `pip install flet-permission-handler` | Runtime permissions   |
| `flet-rive`              | `pip install flet-rive`           | Rive animations           |
| `flet-secure-storage`    | `pip install flet-secure-storage` | Encrypted key-value store |
| `flet-video`             | `pip install flet-video`          | Video playback            |
| `flet-webview`           | `pip install flet-webview`        | Embedded web views        |

---

## Creating Custom Extensions

You can wrap any Flutter/Dart package as a Flet extension:

```bash
# Scaffold an extension project
flet create --template extension --project-name flet-mywidget
```

This creates a project with:
- Python control class
- Flutter/Dart wrapper for the pub.dev package
- Example app in `examples/`

Build and test:

```bash
cd examples/flet_mywidget_example
flet build macos -v        # or windows, linux, web, apk
```

See the [Flet Extensions Guide](https://docs.flet.dev/extend/user-extensions/) for full details.

---

## Publishing & Packaging

Use `flet build` to package your app for distribution:

```bash
# Desktop
flet build windows
flet build macos
flet build linux

# Mobile
flet build apk          # Android APK
flet build aab          # Android App Bundle (Play Store)
flet build ipa          # iOS (requires macOS)

# Web
flet build web          # Static web (WASM/Pyodide)
```

### Build Platform Matrix

| Run `flet build` on | → Android | → iOS | → macOS | → Linux | → Windows | → Web |
| -------------------- | --------- | ----- | ------- | ------- | --------- | ----- |
| **macOS**            | ✅        | ✅    | ✅      |         |           | ✅    |
| **Windows**          | ✅        |       |         | ✅ WSL  | ✅        | ✅    |
| **Linux**            | ✅        |       |         | ✅      |           | ✅    |

**Requirements:** Flutter SDK is needed for building. If not in PATH, it's auto-downloaded on first build.

---

## Server-Side Web (FastAPI)

Flet can run as a server-side web app with real-time UI updates:

```python
import flet as ft
import flet.fastapi as flet_fastapi

async def main(page: ft.Page):
    page.add(ft.Text("Hello from server!"))

app = flet_fastapi.app(main)
```

Run with uvicorn:

```bash
uvicorn main:app
```

Features:
- Real-time UI via WebSocket
- Session management
- PubSub for multi-user apps
- File uploads
- Full FastAPI ecosystem (middleware, auth, static files)

---

## Platform Support Matrix

| Platform | Desktop App | Web (WASM) | Web (Server) | Mobile App |
| -------- | ----------- | ---------- | ------------ | ---------- |
| Windows  | ✅          | ✅         | ✅           | —          |
| macOS    | ✅          | ✅         | ✅           | —          |
| Linux    | ✅          | ✅         | ✅           | —          |
| iOS      | —           | —          | —            | ✅         |
| Android  | —           | —          | —            | ✅         |

---

## CLI Reference

| Command             | Purpose                                         |
| ------------------- | ----------------------------------------------- |
| `flet create`       | Scaffold a new Flet project                     |
| `flet run`          | Run app (desktop by default, `--web` for web)   |
| `flet run -w`       | Run with hot reload watching all files           |
| `flet build <target>` | Package app (apk, ipa, macos, windows, linux, web) |
| `flet publish`      | Publish as static website                       |
| `flet pack`         | Package with PyInstaller (legacy)               |
| `flet doctor`       | Check development environment                   |
| `flet devices`      | List connected devices                          |
| `flet emulators`    | List available emulators                        |

---

## Recommended Project Structure

```
my-flet-app/
├── src/
│   ├── main.py              # Entry point — ft.run(main)
│   ├── views/               # Screen/page views
│   │   ├── home.py
│   │   ├── settings.py
│   │   └── ...
│   ├── components/          # Reusable custom controls
│   │   ├── header.py
│   │   ├── sidebar.py
│   │   └── ...
│   ├── services/            # Business logic, API clients
│   │   └── api.py
│   ├── models/              # Data models
│   │   └── user.py
│   └── assets/              # Images, fonts, icons
│       └── icon.png
├── storage/
│   ├── data/                # App data storage
│   └── temp/                # Temporary files
├── tests/
│   └── test_app.py
├── pyproject.toml
└── README.md
```

---

## Common Patterns & Tips

### Update UI After Modifying Controls

```python
# page.add() auto-updates, but property changes need explicit update:
text = ft.Text("Hello")
page.add(text)
text.value = "Updated"
page.update()              # Required to push changes
```

### Control Refs (Avoid Global Variables)

```python
username = ft.Ref[ft.TextField]()

page.add(ft.TextField(ref=username, label="Name"))

# Access via ref
print(username.current.value)
```

### Dialog Pattern

```python
dialog = ft.AlertDialog(
    title=ft.Text("Confirm"),
    content=ft.Text("Are you sure?"),
    actions=[
        ft.TextButton("Yes", on_click=lambda e: page.close(dialog)),
        ft.TextButton("No", on_click=lambda e: page.close(dialog)),
    ],
)
page.open(dialog)
```

### PubSub (Multi-User Server Apps)

```python
# Subscribe
page.pubsub.subscribe(lambda msg: page.add(ft.Text(msg)))

# Publish to all sessions
page.pubsub.send_all("Hello everyone!")
```

### Window Customization (Desktop)

```python
page.window.width = 800
page.window.height = 600
page.window.title_bar_hidden = True    # Frameless window
page.window.center()
```

### Environment Variables

| Variable            | Purpose                                |
| ------------------- | -------------------------------------- |
| `FLET_SECRET_KEY`   | Encryption key for sessions            |
| `FLET_VIEW_PATH`    | Custom Flutter desktop client path     |
| `FLET_WEB_PATH`     | Custom Flutter web client path         |
| `FLET_FORCE_WEB_VIEW` | Force web view mode                 |

---

## Control Parameters Reference

Below is a comprehensive reference of properties for the most commonly used Flet controls. All controls inherit from base classes — properties from `Control` and `LayoutControl` are available on all derived controls.

> **Note:** Event handler types are shown as `ControlEventHandler[...]` or `EventHandler[...]`. In practice, these are callable functions: `def handler(e): ...`

---

### Base: Control

All controls inherit these properties.

| Property | Type | Default | Description |
|---|---|---|---|
| `key` | `Optional[str]` | `None` | Unique identifier for state management |
| `visible` | `bool` | `True` | Whether control is visible |
| `disabled` | `bool` | `False` | Whether control is disabled |
| `data` | `Any` | `None` | Arbitrary user data attached to control |
| `ref` | `Optional[Ref]` | `None` | Reference for accessing control in code |
| `badge` | `Optional[BadgeValue]` | `None` | Badge displayed on the control |
| `tooltip` | `Optional[TooltipValue]` | `None` | Tooltip shown on hover |
| `opacity` | `Number` | `1.0` | Control opacity (0.0–1.0) |
| `animate_opacity` | `Optional[AnimationValue]` | `None` | Opacity animation config |
| `rotate` | `Optional[RotateValue]` | `None` | Rotation transform |
| `animate_rotation` | `Optional[AnimationValue]` | `None` | Rotation animation config |
| `scale` | `Optional[ScaleValue]` | `None` | Scale transform |
| `animate_scale` | `Optional[AnimationValue]` | `None` | Scale animation config |
| `offset` | `Optional[OffsetValue]` | `None` | Position offset |
| `animate_offset` | `Optional[AnimationValue]` | `None` | Offset animation config |
| `animate_size` | `Optional[AnimationValue]` | `None` | Size change animation config |
| `on_animation_end` | `Optional[EventHandler[...]]` | `None` | Animation completed callback |

### Base: LayoutControl (extends Control)

Controls with layout capabilities inherit these.

| Property | Type | Default | Description |
|---|---|---|---|
| `width` | `Optional[Number]` | `None` | Fixed width |
| `height` | `Optional[Number]` | `None` | Fixed height |
| `expand` | `Optional[Union[bool, int]]` | `None` | Expand to fill space (or flex factor) |
| `expand_loose` | `bool` | `False` | Expand loosely (up to available space) |
| `col` | `Optional[ResponsiveNumber]` | `None` | Column span in `ResponsiveRow` |
| `left` | `Optional[Number]` | `None` | Left position in `Stack` |
| `top` | `Optional[Number]` | `None` | Top position in `Stack` |
| `right` | `Optional[Number]` | `None` | Right position in `Stack` |
| `bottom` | `Optional[Number]` | `None` | Bottom position in `Stack` |

### Base: ScrollableControl (mixin)

Inherited by `View`, `Row`, `Column`, `ListView`, `GridView`.

| Property | Type | Default | Description |
|---|---|---|---|
| `scroll` | `Optional[ScrollMode]` | `None` | Enable scrolling |
| `auto_scroll` | `bool` | `False` | Auto-scroll to end on update |
| `scroll_interval` | `Number` | `10` | Scroll event throttle (ms) |
| `on_scroll` | `Optional[EventHandler[OnScrollEvent]]` | `None` | Scroll position changed |

---

### Page

Top-level application container. Accessed as the `page` parameter in your `main(page)` function.

| Property | Type | Default | Description |
|---|---|---|---|
| `title` | `str` | `""` | Window/browser tab title |
| `route` | `str` | `"/"` | Current navigation route |
| `controls` | `list[Control]` | `[]` | Page body controls |
| `appbar` | `Optional[AppBar]` | `None` | Top application bar |
| `navigation_bar` | `Optional[NavigationBar]` | `None` | Bottom navigation bar |
| `drawer` | `Optional[NavigationDrawer]` | `None` | Left side drawer |
| `end_drawer` | `Optional[NavigationDrawer]` | `None` | Right side drawer |
| `floating_action_button` | `Optional[FloatingActionButton]` | `None` | Floating action button |
| `floating_action_button_location` | `Optional[FloatingActionButtonLocation]` | `None` | FAB position |
| `bottom_appbar` | `Optional[BottomAppBar]` | `None` | Bottom app bar |
| `bottom_sheet` | `Optional[BottomSheet]` | `None` | Persistent bottom sheet |
| `dialog` | `Optional[Control]` | `None` | Active dialog control |
| `overlay` | `list[Control]` | `[]` | Overlay controls on top of page |
| `snack_bar` | `Optional[SnackBar]` | `None` | Snack bar notification |
| `banner` | `Optional[Banner]` | `None` | Top banner |
| `bgcolor` | `Optional[ColorValue]` | `None` | Background color |
| `theme` | `Optional[Theme]` | `None` | Light theme config |
| `dark_theme` | `Optional[Theme]` | `None` | Dark theme config |
| `theme_mode` | `Optional[ThemeMode]` | `None` | Light/dark/system mode |
| `locale_configuration` | `Optional[LocaleConfiguration]` | `None` | Locale settings |
| `rtl` | `bool` | `False` | Right-to-left layout |
| `fonts` | `Optional[dict[str, str]]` | `None` | Custom font families |
| `padding` | `PaddingValue` | `10` | Page body padding |
| `spacing` | `Number` | `10` | Spacing between body controls |
| `horizontal_alignment` | `CrossAxisAlignment` | `START` | Horizontal body alignment |
| `vertical_alignment` | `MainAxisAlignment` | `START` | Vertical body alignment |
| `debug` | `bool` | `False` | Show performance overlay |
| `on_route_change` | `Optional[EventHandler[...]]` | `None` | Route changed |
| `on_view_pop` | `Optional[EventHandler[...]]` | `None` | View popped |
| `on_resize` | `Optional[EventHandler[...]]` | `None` | Page resized |
| `on_platform_brightness_change` | `Optional[EventHandler[...]]` | `None` | Brightness changed |
| `on_keyboard_event` | `Optional[EventHandler[...]]` | `None` | Keyboard event |
| `on_scroll` | `Optional[EventHandler[...]]` | `None` | Page scrolled |
| `on_connect` | `Optional[EventHandler[...]]` | `None` | Client connected |
| `on_disconnect` | `Optional[EventHandler[...]]` | `None` | Client disconnected |
| `on_error` | `Optional[EventHandler[...]]` | `None` | Unhandled error |
| `on_close` | `Optional[EventHandler[...]]` | `None` | Session closing |

### View

A screen within the navigation stack. Added to `page.views`.

| Property | Type | Default | Description |
|---|---|---|---|
| `controls` | `list[Control]` | `[]` | View body controls |
| `route` | `str` | `""` | View route path |
| `appbar` | `Optional[AppBar]` | `None` | Top application bar |
| `navigation_bar` | `Optional[NavigationBar]` | `None` | Bottom navigation bar |
| `drawer` | `Optional[NavigationDrawer]` | `None` | Left side drawer |
| `end_drawer` | `Optional[NavigationDrawer]` | `None` | Right side drawer |
| `floating_action_button` | `Optional[FloatingActionButton]` | `None` | Floating action button |
| `floating_action_button_location` | `Optional[FloatingActionButtonLocation]` | `None` | FAB position |
| `bottom_appbar` | `Optional[BottomAppBar]` | `None` | Bottom app bar |
| `bottom_sheet` | `Optional[BottomSheet]` | `None` | Persistent bottom sheet |
| `bgcolor` | `Optional[ColorValue]` | `None` | Background color |
| `padding` | `PaddingValue` | `10` | Body padding |
| `spacing` | `Number` | `10` | Spacing between controls |
| `horizontal_alignment` | `CrossAxisAlignment` | `START` | Horizontal alignment |
| `vertical_alignment` | `MainAxisAlignment` | `START` | Vertical alignment |
| `fullscreen_dialog` | `bool` | `False` | Fullscreen dialog mode |

---

### Container

A versatile styling wrapper for a single child control.

| Property | Type | Default | Description |
|---|---|---|---|
| `content` | `Optional[Control]` | `None` | Child control |
| `padding` | `Optional[PaddingValue]` | `None` | Inner padding |
| `margin` | `Optional[MarginValue]` | `None` | Outer margin |
| `alignment` | `Optional[Alignment]` | `None` | Child alignment |
| `bgcolor` | `Optional[ColorValue]` | `None` | Background color |
| `gradient` | `Optional[Gradient]` | `None` | Background gradient |
| `border` | `Optional[Border]` | `None` | Border around container |
| `border_radius` | `Optional[BorderRadiusValue]` | `None` | Rounded corners |
| `shadow` | `Optional[list[BoxShadow]]` | `None` | Drop shadows |
| `shape` | `Optional[BoxShape]` | `None` | Box shape (rectangle/circle) |
| `clip_behavior` | `ClipBehavior` | `ANTI_ALIAS` | Content clipping mode |
| `blend_mode` | `Optional[BlendMode]` | `None` | Painting blend mode |
| `ink` | `bool` | `False` | Material ink ripple effect |
| `ink_color` | `Optional[ColorValue]` | `None` | Ink splash color |
| `color_filter` | `Optional[ColorFilter]` | `None` | Color filter applied |
| `image` | `Optional[DecorationImage]` | `None` | Background image |
| `foreground_image` | `Optional[DecorationImage]` | `None` | Foreground image |
| `theme` | `Optional[Theme]` | `None` | Override theme for children |
| `dark_theme` | `Optional[Theme]` | `None` | Override dark theme |
| `theme_mode` | `Optional[ThemeMode]` | `None` | Theme mode override |
| `url` | `Optional[Union[str, Url]]` | `None` | URL to open on click |
| `ignore_interactions` | `bool` | `False` | Ignore pointer events |
| `animate` | `Optional[AnimationValue]` | `None` | Implicit animation config |
| `on_click` | `Optional[ControlEventHandler[...]]` | `None` | Click handler |
| `on_tap_down` | `Optional[EventHandler[...]]` | `None` | Tap-down handler |
| `on_long_press` | `Optional[ControlEventHandler[...]]` | `None` | Long press handler |
| `on_hover` | `Optional[EventHandler[...]]` | `None` | Hover state handler |

---

### Row

Arranges children horizontally.

| Property | Type | Default | Description |
|---|---|---|---|
| `controls` | `list[Control]` | `[]` | Child controls |
| `alignment` | `MainAxisAlignment` | `START` | Horizontal alignment |
| `vertical_alignment` | `CrossAxisAlignment` | `START` | Vertical alignment |
| `spacing` | `Number` | `10` | Spacing between children |
| `tight` | `bool` | `False` | Minimize occupied space |
| `wrap` | `bool` | `False` | Wrap to next line |
| `run_spacing` | `Number` | `10` | Spacing between wrapped lines |
| `clip_behavior` | `ClipBehavior` | `NONE` | Content clipping |

### Column

Arranges children vertically.

| Property | Type | Default | Description |
|---|---|---|---|
| `controls` | `list[Control]` | `[]` | Child controls |
| `alignment` | `MainAxisAlignment` | `START` | Vertical alignment |
| `horizontal_alignment` | `CrossAxisAlignment` | `START` | Horizontal alignment |
| `spacing` | `Number` | `10` | Spacing between children |
| `tight` | `bool` | `False` | Minimize occupied space |
| `wrap` | `bool` | `False` | Wrap to next column |
| `run_spacing` | `Number` | `10` | Spacing between wrapped columns |
| `clip_behavior` | `ClipBehavior` | `NONE` | Content clipping |

### Stack

Overlays children on top of each other.

| Property | Type | Default | Description |
|---|---|---|---|
| `controls` | `list[Control]` | `[]` | Stacked children (LIFO order) |
| `clip_behavior` | `ClipBehavior` | `HARD_EDGE` | Content clipping |
| `alignment` | `Optional[Alignment]` | `None` | Non-positioned children alignment |
| `fit` | `StackFit` | `LOOSE` | Non-positioned children sizing |

### ResponsiveRow

12-column responsive grid layout (Bootstrap-style).

| Property | Type | Default | Description |
|---|---|---|---|
| `controls` | `list[Control]` | `[]` | Child controls |
| `columns` | `ResponsiveNumber` | `12` | Virtual column count |
| `alignment` | `MainAxisAlignment` | `START` | Horizontal child placement |
| `vertical_alignment` | `CrossAxisAlignment` | `START` | Vertical child placement |
| `spacing` | `ResponsiveNumber` | `10` | Spacing within a row |
| `run_spacing` | `ResponsiveNumber` | `10` | Spacing between rows |
| `breakpoints` | `dict` | *(Bootstrap defaults)* | Breakpoint width definitions |

### ListView

Scrollable list of controls.

| Property | Type | Default | Description |
|---|---|---|---|
| `controls` | `list[Control]` | `[]` | Child controls |
| `horizontal` | `bool` | `False` | Horizontal layout |
| `reverse` | `bool` | `False` | Reverse scroll direction |
| `spacing` | `Number` | `0` | Divider height between items |
| `item_extent` | `Optional[Number]` | `None` | Fixed item height/width |
| `first_item_prototype` | `bool` | `False` | Use first item as prototype size |
| `padding` | `Optional[PaddingValue]` | `None` | Content padding |
| `clip_behavior` | `ClipBehavior` | `HARD_EDGE` | Content clipping |
| `cache_extent` | `Optional[Number]` | `None` | Off-screen cache pixels |
| `build_controls_on_demand` | `bool` | `True` | Lazy/on-demand building |

### GridView

Scrollable 2D grid of controls.

| Property | Type | Default | Description |
|---|---|---|---|
| `controls` | `list[Control]` | `[]` | Child controls |
| `horizontal` | `bool` | `False` | Horizontal layout |
| `reverse` | `bool` | `False` | Reverse scroll direction |
| `runs_count` | `int` | `1` | Cross-axis children count |
| `max_extent` | `Optional[int]` | `None` | Max item width/height |
| `spacing` | `Number` | `10` | Main-axis spacing |
| `run_spacing` | `Number` | `10` | Cross-axis spacing |
| `child_aspect_ratio` | `Number` | `1.0` | Cross-to-main axis ratio |
| `padding` | `Optional[PaddingValue]` | `None` | Content padding |
| `cache_extent` | `Optional[Number]` | `None` | Off-screen cache pixels |
| `build_controls_on_demand` | `bool` | `True` | Lazy/on-demand building |

### SafeArea

Insets child to avoid OS intrusions (notches, status bars).

| Property | Type | Default | Description |
|---|---|---|---|
| `content` | `Control` | *(required)* | Child control |
| `avoid_intrusions_left` | `bool` | `True` | Avoid left intrusions |
| `avoid_intrusions_top` | `bool` | `True` | Avoid top intrusions |
| `avoid_intrusions_right` | `bool` | `True` | Avoid right intrusions |
| `avoid_intrusions_bottom` | `bool` | `True` | Avoid bottom intrusions |
| `minimum_padding` | `PaddingValue` | `0` | Minimum padding applied |

---

### Text

Displays styled text.

| Property | Type | Default | Description |
|---|---|---|---|
| `value` | `str` | `""` | Text content |
| `size` | `Optional[Number]` | `None` | Font size |
| `weight` | `Optional[FontWeight]` | `None` | Font weight (bold, normal, etc.) |
| `italic` | `bool` | `False` | Italic style |
| `font_family` | `Optional[str]` | `None` | Font family name |
| `color` | `Optional[ColorValue]` | `None` | Text color |
| `bgcolor` | `Optional[ColorValue]` | `None` | Background color |
| `text_align` | `Optional[TextAlign]` | `None` | Text alignment |
| `overflow` | `Optional[TextOverflow]` | `None` | Overflow handling |
| `max_lines` | `Optional[int]` | `None` | Maximum line count |
| `selectable` | `bool` | `False` | User-selectable text |
| `no_wrap` | `bool` | `False` | Disable text wrapping |
| `style` | `Optional[TextStyle]` | `None` | Full text style object |
| `spans` | `Optional[list[InlineSpan]]` | `None` | Rich text spans |
| `semantics_label` | `Optional[str]` | `None` | Accessibility label |

### TextField

Text input field with rich configuration.

| Property | Type | Default | Description |
|---|---|---|---|
| `value` | `str` | `""` | Current text value |
| `label` | `Optional[StrOrControl]` | `None` | Input field label |
| `hint_text` | `Optional[str]` | `None` | Placeholder hint text |
| `helper_text` | `Optional[str]` | `None` | Helper text below field |
| `error_text` | `Optional[str]` | `None` | Error message below field |
| `prefix` | `Optional[Control]` | `None` | Prefix control |
| `prefix_icon` | `Optional[IconDataOrControl]` | `None` | Leading icon |
| `prefix_text` | `Optional[str]` | `None` | Prefix text |
| `suffix` | `Optional[Control]` | `None` | Suffix control |
| `suffix_icon` | `Optional[IconDataOrControl]` | `None` | Trailing icon |
| `suffix_text` | `Optional[str]` | `None` | Suffix text |
| `password` | `bool` | `False` | Obscure text input |
| `can_reveal_password` | `bool` | `False` | Show toggle to reveal password |
| `multiline` | `bool` | `False` | Allow multi-line input |
| `min_lines` | `Optional[int]` | `None` | Minimum visible lines |
| `max_lines` | `Optional[int]` | `None` | Maximum visible lines |
| `max_length` | `Optional[int]` | `None` | Maximum character count |
| `read_only` | `bool` | `False` | Non-editable display |
| `autofocus` | `bool` | `False` | Focus on creation |
| `keyboard_type` | `KeyboardType` | `TEXT` | Virtual keyboard type |
| `text_align` | `TextAlign` | `LEFT` | Text alignment |
| `text_size` | `Optional[Number]` | `None` | Text font size |
| `text_style` | `Optional[TextStyle]` | `None` | Text style |
| `color` | `Optional[ColorValue]` | `None` | Text color |
| `bgcolor` | `Optional[ColorValue]` | `None` | Background color |
| `border` | `Optional[InputBorder]` | `None` | Border type |
| `border_radius` | `Optional[BorderRadiusValue]` | `None` | Border radius |
| `border_width` | `Number` | `1` | Border width |
| `border_color` | `Optional[ColorValue]` | `None` | Border color |
| `focused_border_width` | `Optional[Number]` | `None` | Focused border width |
| `focused_border_color` | `Optional[ColorValue]` | `None` | Focused border color |
| `content_padding` | `Optional[PaddingValue]` | `None` | Inner content padding |
| `dense` | `bool` | `False` | Dense/compact layout |
| `filled` | `bool` | `False` | Filled background style |
| `fill_color` | `Optional[ColorValue]` | `None` | Fill color |
| `counter_text` | `Optional[str]` | `None` | Character counter text |
| `capitalization` | `Optional[TextCapitalization]` | `None` | Auto-capitalization mode |
| `input_filter` | `Optional[InputFilter]` | `None` | Input text filter |
| `enable_suggestions` | `bool` | `True` | Keyboard suggestions |
| `autocorrect` | `bool` | `True` | Autocorrect mode |
| `smart_dashes_type` | `bool` | `True` | Smart dashes |
| `smart_quotes_type` | `bool` | `True` | Smart quotes |
| `cursor_color` | `Optional[ColorValue]` | `None` | Cursor color |
| `cursor_width` | `Optional[Number]` | `None` | Cursor width |
| `cursor_height` | `Optional[Number]` | `None` | Cursor height |
| `cursor_radius` | `Optional[Number]` | `None` | Cursor radius |
| `selection_color` | `Optional[ColorValue]` | `None` | Text selection color |
| `text_vertical_align` | `Optional[Union[VerticalAlignment, Number]]` | `None` | Vertical text alignment |
| `on_change` | `Optional[ControlEventHandler[...]]` | `None` | Text changed |
| `on_submit` | `Optional[ControlEventHandler[...]]` | `None` | Enter key pressed |
| `on_focus` | `Optional[ControlEventHandler[...]]` | `None` | Focus gained |
| `on_blur` | `Optional[ControlEventHandler[...]]` | `None` | Focus lost |

### Dropdown

Dropdown selection menu.

| Property | Type | Default | Description |
|---|---|---|---|
| `options` | `list[Option]` | `[]` | Selectable options |
| `value` | `str` | `""` | Current selected value |
| `editable` | `bool` | `False` | Allow text editing |
| `menu_height` | `Optional[Number]` | `None` | Menu height |
| `menu_width` | `Optional[Number]` | `None` | Menu width |
| `menu_style` | `Optional[MenuStyle]` | `None` | Menu visual attributes |
| `label` | `Optional[StrOrControl]` | `None` | Input field description |
| `hint_text` | `Optional[str]` | `None` | Placeholder hint text |
| `error_text` | `Optional[str]` | `None` | Error message below field |
| `trailing_icon` | `Optional[IconDataOrControl]` | `None` | Icon at field end |
| `leading_icon` | `Optional[IconDataOrControl]` | `None` | Icon at field start |
| `border` | `Optional[InputBorder]` | `None` | Border type |
| `border_radius` | `Optional[BorderRadiusValue]` | `None` | Border radius |
| `border_width` | `Number` | `1` | Border width |
| `border_color` | `Optional[ColorValue]` | `None` | Border color |
| `content_padding` | `Optional[PaddingValue]` | `None` | Container padding |
| `dense` | `bool` | `False` | Dense form layout |
| `filled` | `bool` | `False` | Filled background |
| `fill_color` | `Optional[ColorValue]` | `None` | Background fill color |
| `color` | `Optional[ColorValue]` | `None` | Text color |
| `text_size` | `Optional[Number]` | `None` | Text size |
| `text_style` | `Optional[TextStyle]` | `None` | Text input style |
| `capitalization` | `Optional[TextCapitalization]` | `None` | Text capitalization |
| `input_filter` | `Optional[InputFilter]` | `None` | Text input filter |
| `on_select` | `Optional[ControlEventHandler[...]]` | `None` | Selection changed |
| `on_text_change` | `Optional[ControlEventHandler[...]]` | `None` | Text input changed |
| `on_focus` | `Optional[ControlEventHandler[...]]` | `None` | Focus gained |
| `on_blur` | `Optional[ControlEventHandler[...]]` | `None` | Focus lost |

### Checkbox

Toggle checkbox with optional label.

| Property | Type | Default | Description |
|---|---|---|---|
| `value` | `bool` | `False` | Checked state |
| `tristate` | `bool` | `False` | Allow indeterminate (null) state |
| `label` | `str` | `""` | Clickable label text |
| `label_position` | `LabelPosition` | `RIGHT` | Label side |
| `label_style` | `Optional[TextStyle]` | `None` | Label text style |
| `autofocus` | `bool` | `False` | Focus on creation |
| `active_color` | `Optional[ColorValue]` | `None` | Color when checked |
| `check_color` | `Optional[ColorValue]` | `None` | Checkmark color |
| `fill_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Fill color by state |
| `overlay_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Overlay color by state |
| `hover_color` | `Optional[ColorValue]` | `None` | Color when hovered |
| `focus_color` | `Optional[ColorValue]` | `None` | Color when focused |
| `shape` | `Optional[OutlinedBorder]` | `None` | Checkbox shape |
| `splash_radius` | `Optional[Number]` | `None` | Ink splash radius |
| `border_side` | `Optional[BorderSide]` | `None` | Outline border side |
| `is_error` | `bool` | `False` | Show error state |
| `semantics_label` | `Optional[str]` | `None` | Accessibility label |
| `visual_density` | `Optional[VisualDensity]` | `None` | Layout compactness |
| `mouse_cursor` | `Optional[MouseCursor]` | `None` | Mouse cursor style |
| `on_change` | `Optional[ControlEventHandler[...]]` | `None` | Value changed |
| `on_focus` | `Optional[ControlEventHandler[...]]` | `None` | Focus gained |
| `on_blur` | `Optional[ControlEventHandler[...]]` | `None` | Focus lost |

### Switch

Toggle switch with optional label.

| Property | Type | Default | Description |
|---|---|---|---|
| `value` | `bool` | `False` | On/off state |
| `label` | `str` | `""` | Clickable label text |
| `label_position` | `LabelPosition` | `RIGHT` | Label side |
| `label_style` | `Optional[TextStyle]` | `None` | Label text style |
| `autofocus` | `bool` | `False` | Focus on creation |
| `active_color` | `Optional[ColorValue]` | `None` | Track color when on |
| `active_track_color` | `Optional[ColorValue]` | `None` | Track color when on |
| `inactive_thumb_color` | `Optional[ColorValue]` | `None` | Thumb when off |
| `inactive_track_color` | `Optional[ColorValue]` | `None` | Track color when off |
| `thumb_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Thumb color by state |
| `track_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Track color by state |
| `thumb_icon` | `Optional[ControlStateValue[IconDataOrControl]]` | `None` | Thumb icon by state |
| `overlay_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Overlay by state |
| `hover_color` | `Optional[ColorValue]` | `None` | Color when hovered |
| `focus_color` | `Optional[ColorValue]` | `None` | Color when focused |
| `splash_radius` | `Optional[Number]` | `None` | Ink splash radius |
| `track_outline_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Track outline by state |
| `track_outline_width` | `Optional[ControlStateValue[Number]]` | `None` | Track outline width |
| `mouse_cursor` | `Optional[MouseCursor]` | `None` | Mouse cursor style |
| `on_change` | `Optional[ControlEventHandler[...]]` | `None` | Value changed |
| `on_focus` | `Optional[ControlEventHandler[...]]` | `None` | Focus gained |
| `on_blur` | `Optional[ControlEventHandler[...]]` | `None` | Focus lost |

### Radio

Radio button for use inside `RadioGroup`.

| Property | Type | Default | Description |
|---|---|---|---|
| `label` | `str` | `""` | Clickable label text |
| `label_position` | `LabelPosition` | `RIGHT` | Label side |
| `label_style` | `Optional[TextStyle]` | `None` | Label text style |
| `value` | `Optional[str]` | `None` | Value for RadioGroup |
| `autofocus` | `bool` | `False` | Focus on creation |
| `fill_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Fill color by state |
| `active_color` | `Optional[ColorValue]` | `None` | Color when selected |
| `overlay_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Overlay color by state |
| `hover_color` | `Optional[ColorValue]` | `None` | Color when hovered |
| `focus_color` | `Optional[ColorValue]` | `None` | Color when focused |
| `splash_radius` | `Optional[Number]` | `None` | Ink splash radius |
| `toggleable` | `bool` | `False` | Allow deselect on re-tap |
| `visual_density` | `Optional[VisualDensity]` | `None` | Layout compactness |
| `mouse_cursor` | `Optional[MouseCursor]` | `None` | Mouse cursor style |
| `on_focus` | `Optional[ControlEventHandler[...]]` | `None` | Focus gained |
| `on_blur` | `Optional[ControlEventHandler[...]]` | `None` | Focus lost |

### Slider

Continuous or discrete value slider.

| Property | Type | Default | Description |
|---|---|---|---|
| `value` | `Optional[Number]` | `None` | Current slider value |
| `label` | `Optional[str]` | `None` | Label above slider (with `{value}`) |
| `min` | `Number` | `0.0` | Minimum value |
| `max` | `Number` | `1.0` | Maximum value |
| `divisions` | `Optional[int]` | `None` | Discrete division count |
| `round` | `int` | `0` | Decimal places on label |
| `autofocus` | `bool` | `False` | Focus on creation |
| `active_color` | `Optional[ColorValue]` | `None` | Active track color |
| `inactive_color` | `Optional[ColorValue]` | `None` | Inactive track color |
| `thumb_color` | `Optional[ColorValue]` | `None` | Thumb color |
| `interaction` | `Optional[SliderInteraction]` | `None` | Interaction mode |
| `overlay_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Highlight color by state |
| `mouse_cursor` | `Optional[MouseCursor]` | `None` | Mouse cursor style |
| `on_change` | `Optional[ControlEventHandler[...]]` | `None` | Value changed |
| `on_change_start` | `Optional[ControlEventHandler[...]]` | `None` | Drag started |
| `on_change_end` | `Optional[ControlEventHandler[...]]` | `None` | Drag ended |
| `on_focus` | `Optional[ControlEventHandler[...]]` | `None` | Focus gained |
| `on_blur` | `Optional[ControlEventHandler[...]]` | `None` | Focus lost |

---

### Button

Standard Material button (ElevatedButton-style).

| Property | Type | Default | Description |
|---|---|---|---|
| `content` | `Optional[StrOrControl]` | `None` | Button content (text or control) |
| `icon` | `Optional[IconDataOrControl]` | `None` | Leading icon |
| `icon_color` | `Optional[ColorValue]` | `None` | Icon color |
| `style` | `Optional[ButtonStyle]` | `None` | Full button style |
| `autofocus` | `bool` | `False` | Focus on creation |
| `url` | `Optional[Union[str, Url]]` | `None` | URL to open on click |
| `on_click` | `Optional[ControlEventHandler[...]]` | `None` | Click handler |
| `on_long_press` | `Optional[ControlEventHandler[...]]` | `None` | Long press handler |
| `on_hover` | `Optional[EventHandler[...]]` | `None` | Hover state handler |
| `on_focus` | `Optional[ControlEventHandler[...]]` | `None` | Focus gained |
| `on_blur` | `Optional[ControlEventHandler[...]]` | `None` | Focus lost |

### IconButton

A button with an icon only.

| Property | Type | Default | Description |
|---|---|---|---|
| `content` | `Optional[StrOrControl]` | `None` | Button content |
| `icon` | `Optional[IconDataOrControl]` | `None` | Button icon |
| `icon_size` | `Optional[Number]` | `None` | Icon size |
| `icon_color` | `Optional[ColorValue]` | `None` | Default icon color |
| `selected` | `bool` | `False` | Toggle selected state |
| `selected_icon` | `Optional[IconDataOrControl]` | `None` | Icon when selected |
| `selected_icon_color` | `Optional[ColorValue]` | `None` | Color when selected |
| `bgcolor` | `Optional[ColorValue]` | `None` | Background color |
| `highlight_color` | `Optional[ColorValue]` | `None` | Highlight color on press |
| `style` | `Optional[ButtonStyle]` | `None` | Full button style |
| `autofocus` | `bool` | `False` | Focus on creation |
| `enable_feedback` | `Optional[bool]` | `None` | Haptic feedback |
| `alignment` | `Optional[Alignment]` | `None` | Icon alignment |
| `padding` | `Optional[PaddingValue]` | `None` | Internal padding |
| `visual_density` | `Optional[VisualDensity]` | `None` | Layout compactness |
| `mouse_cursor` | `Optional[MouseCursor]` | `None` | Mouse cursor style |
| `url` | `Optional[Union[str, Url]]` | `None` | URL to open on click |
| `on_click` | `Optional[ControlEventHandler[...]]` | `None` | Click handler |
| `on_focus` | `Optional[ControlEventHandler[...]]` | `None` | Focus gained |
| `on_blur` | `Optional[ControlEventHandler[...]]` | `None` | Focus lost |

### FloatingActionButton

Primary action button (FAB).

| Property | Type | Default | Description |
|---|---|---|---|
| `content` | `Optional[StrOrControl]` | `None` | Button content |
| `icon` | `Optional[IconDataOrControl]` | `None` | Button icon |
| `bgcolor` | `Optional[ColorValue]` | `None` | Background color |
| `shape` | `Optional[OutlinedBorder]` | `None` | Border shape |
| `autofocus` | `bool` | `False` | Focus on creation |
| `mini` | `bool` | `False` | Small (40px) variant |
| `foreground_color` | `Optional[ColorValue]` | `None` | Icon/text foreground color |
| `elevation` | `Optional[Number]` | `None` | Default elevation |
| `hover_elevation` | `Optional[Number]` | `None` | Hover elevation |
| `focus_elevation` | `Optional[Number]` | `None` | Focus elevation |
| `highlight_elevation` | `Optional[Number]` | `None` | Highlight elevation |
| `clip_behavior` | `ClipBehavior` | `NONE` | Content clipping |
| `url` | `Optional[Union[str, Url]]` | `None` | URL to open on click |
| `mouse_cursor` | `Optional[MouseCursor]` | `None` | Mouse cursor style |
| `on_click` | `Optional[ControlEventHandler[...]]` | `None` | Click handler |

---

### Image

Displays an image from URL, asset, or file path.

| Property | Type | Default | Description |
|---|---|---|---|
| `src` | `Optional[str]` | `None` | Image URL, asset path, or file path |
| `src_base64` | `Optional[str]` | `None` | Base64-encoded image data |
| `error_content` | `Optional[Control]` | `None` | Fallback on load error |
| `fit` | `Optional[ImageFit]` | `None` | Image scaling mode |
| `repeat` | `ImageRepeat` | `NO_REPEAT` | Image tiling mode |
| `color` | `Optional[ColorValue]` | `None` | Color blend |
| `color_blend_mode` | `Optional[BlendMode]` | `None` | Color blending mode |
| `border_radius` | `Optional[BorderRadiusValue]` | `None` | Rounded corners |
| `filter_quality` | `FilterQuality` | `LOW` | Rendering quality |
| `semantics_label` | `Optional[str]` | `None` | Accessibility label |
| `exclude_from_semantics` | `bool` | `False` | Exclude from accessibility |
| `gapless_playback` | `bool` | `False` | Keep old image during reload |

### Icon

Displays a Material icon.

| Property | Type | Default | Description |
|---|---|---|---|
| `name` | `Optional[IconData]` | `None` | Icon name (e.g., `ft.Icons.HOME`) |
| `color` | `Optional[ColorValue]` | `None` | Icon color |
| `size` | `Optional[Number]` | `None` | Icon size |
| `weight` | `Optional[Number]` | `None` | Icon weight |
| `fill` | `Optional[Number]` | `None` | Fill amount |
| `grade` | `Optional[Number]` | `None` | Icon grade |
| `optical_size` | `Optional[Number]` | `None` | Optical size |
| `semantics_label` | `Optional[str]` | `None` | Accessibility label |

### Markdown

Renders Markdown content.

| Property | Type | Default | Description |
|---|---|---|---|
| `value` | `str` | `""` | Markdown content to render |
| `selectable` | `bool` | `False` | Text is selectable |
| `extension_set` | `MarkdownExtensionSet` | `NONE` | Markdown syntax extensions |
| `code_theme` | `Optional[Union[MarkdownCodeTheme, MarkdownCustomCodeTheme]]` | `None` | Code block syntax theme |
| `auto_follow_links` | `bool` | `False` | Auto-open URLs |
| `shrink_wrap` | `bool` | `True` | Size by contents |
| `fit_content` | `bool` | `True` | Fit to child content |
| `soft_line_break` | `bool` | `False` | Soft line break handling |
| `md_style_sheet` | `Optional[MarkdownStyleSheet]` | `None` | Markdown element styles |
| `code_style_sheet` | `Optional[MarkdownStyleSheet]` | `None` | Code block styles |
| `on_tap_link` | `Optional[ControlEventHandler[...]]` | `None` | Link clicked |
| `on_tap_text` | `Optional[ControlEventHandler[...]]` | `None` | Text clicked |

---

### AppBar

Top application bar.

| Property | Type | Default | Description |
|---|---|---|---|
| `leading` | `Optional[Control]` | `None` | Control before title |
| `leading_width` | `Optional[Number]` | `None` | Leading control width |
| `automatically_imply_leading` | `bool` | `True` | Auto-create leading control |
| `title` | `Optional[StrOrControl]` | `None` | Primary title |
| `center_title` | `Optional[bool]` | `None` | Center the title |
| `toolbar_height` | `Optional[Number]` | `None` | Toolbar height |
| `color` | `Optional[ColorValue]` | `None` | Default text/icon color |
| `bgcolor` | `Optional[ColorValue]` | `None` | Background color |
| `elevation` | `Optional[Number]` | `None` | Bar elevation |
| `elevation_on_scroll` | `Optional[Number]` | `None` | Elevation when scrolled |
| `shadow_color` | `Optional[ColorValue]` | `None` | Shadow color |
| `actions` | `Optional[list[Control]]` | `None` | Row of action controls |
| `title_spacing` | `Optional[Number]` | `None` | Spacing around title |
| `title_text_style` | `Optional[TextStyle]` | `None` | Title text style |
| `toolbar_text_style` | `Optional[TextStyle]` | `None` | Toolbar text style |
| `shape` | `Optional[OutlinedBorder]` | `None` | Material shape |

### NavigationBar

Bottom navigation bar.

| Property | Type | Default | Description |
|---|---|---|---|
| `destinations` | `list[NavigationBarDestination]` | `[]` | Destination items |
| `selected_index` | `int` | `0` | Currently selected index |
| `bgcolor` | `Optional[ColorValue]` | `None` | Bar background color |
| `label_behavior` | `Optional[NavigationBarLabelBehavior]` | `None` | Label display mode |
| `elevation` | `Optional[Number]` | `None` | Bar elevation |
| `shadow_color` | `Optional[ColorValue]` | `None` | Shadow color |
| `indicator_color` | `Optional[ColorValue]` | `None` | Selected indicator color |
| `indicator_shape` | `Optional[OutlinedBorder]` | `None` | Indicator shape |
| `border` | `Optional[Border]` | `None` | Bar border |
| `animation_duration` | `Optional[DurationValue]` | `None` | Transition duration |
| `overlay_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Highlight color by state |
| `on_change` | `Optional[ControlEventHandler[...]]` | `None` | Destination changed |

### Tabs / TabBar / Tab

Tabbed interface controls.

**Tabs** — Wrapper that manages tab controller:

| Property | Type | Default | Description |
|---|---|---|---|
| `content` | `Control` | *(required)* | Content to display |
| `length` | `int` | *(required)* | Total number of tabs |
| `selected_index` | `int` | `0` | Currently selected tab |
| `animation_duration` | `DurationValue` | `Duration(ms=100)` | Tab animation duration |
| `on_change` | `Optional[ControlEventHandler[...]]` | `None` | Tab changed |

**TabBar** — Row of tab buttons:

| Property | Type | Default | Description |
|---|---|---|---|
| `tabs` | `list[Control]` | *(required)* | Tab controls list |
| `scrollable` | `bool` | `True` | Horizontally scrollable |
| `tab_alignment` | `Optional[TabAlignment]` | `None` | Tab alignment |
| `divider_color` | `Optional[ColorValue]` | `None` | Divider color |
| `indicator_color` | `Optional[ColorValue]` | `None` | Selected indicator color |
| `indicator_size` | `Optional[TabBarIndicatorSize]` | `None` | Indicator sizing |
| `indicator_thickness` | `Number` | `2.0` | Indicator line thickness |
| `secondary` | `bool` | `False` | Secondary/nested tab bar |
| `label_color` | `Optional[ColorValue]` | `None` | Selected label color |
| `label_padding` | `Optional[PaddingValue]` | `None` | Label padding |
| `unselected_label_color` | `Optional[ColorValue]` | `None` | Unselected label color |
| `overlay_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Ink response colors |
| `on_click` | `Optional[ControlEventHandler[...]]` | `None` | Tab clicked |

**Tab** — Individual tab:

| Property | Type | Default | Description |
|---|---|---|---|
| `label` | `Optional[StrOrControl]` | `None` | Tab name |
| `icon` | `Optional[IconDataOrControl]` | `None` | Tab icon |
| `height` | `Optional[Number]` | `None` | Tab height |

---

### Card

Material card with elevation.

| Property | Type | Default | Description |
|---|---|---|---|
| `content` | `Optional[Control]` | `None` | Card content |
| `elevation` | `Optional[Number]` | `None` | Shadow elevation |
| `bgcolor` | `Optional[ColorValue]` | `None` | Background color |
| `shadow_color` | `Optional[ColorValue]` | `None` | Shadow color |
| `shape` | `Optional[OutlinedBorder]` | `None` | Border shape |
| `clip_behavior` | `Optional[ClipBehavior]` | `None` | Content clipping |
| `variant` | `CardVariant` | `ELEVATED` | Card style variant |

### AlertDialog

Modal or non-modal dialog.

| Property | Type | Default | Description |
|---|---|---|---|
| `content` | `Optional[Control]` | `None` | Dialog body content |
| `modal` | `bool` | `False` | Block outside dismissal |
| `title` | `Optional[StrOrControl]` | `None` | Dialog title |
| `actions` | `list[Control]` | `[]` | Bottom action buttons |
| `bgcolor` | `Optional[ColorValue]` | `None` | Background color |
| `elevation` | `Optional[Number]` | `None` | Dialog elevation |
| `icon` | `Optional[Control]` | `None` | Icon at top |
| `title_padding` | `Optional[PaddingValue]` | `None` | Padding around title |
| `content_padding` | `Optional[PaddingValue]` | `None` | Padding around content |
| `actions_padding` | `Optional[PaddingValue]` | `None` | Padding around actions |
| `actions_alignment` | `Optional[MainAxisAlignment]` | `None` | Actions horizontal layout |
| `shape` | `Optional[OutlinedBorder]` | `None` | Dialog shape |
| `inset_padding` | `Optional[PaddingValue]` | `None` | Padding around dialog |
| `scrollable` | `bool` | `False` | Scrollable title/content |
| `barrier_color` | `Optional[ColorValue]` | `None` | Modal barrier color |
| `semantics_label` | `Optional[str]` | `None` | Accessibility label |
| `clip_behavior` | `ClipBehavior` | `NONE` | Content clipping |

### SnackBar

Brief notification at bottom of screen.

| Property | Type | Default | Description |
|---|---|---|---|
| `content` | `StrOrControl` | *(required)* | Primary message content |
| `behavior` | `Optional[SnackBarBehavior]` | `None` | Fixed or floating |
| `dismiss_direction` | `Optional[DismissDirection]` | `None` | Swipe dismiss direction |
| `show_close_icon` | `bool` | `False` | Include close icon |
| `action` | `Union[str, SnackBarAction, None]` | `None` | Action button |
| `bgcolor` | `Optional[ColorValue]` | `None` | Background color |
| `duration` | `DurationValue` | `Duration(ms=4000)` | Display duration |
| `margin` | `Optional[MarginValue]` | `None` | Margin (floating only) |
| `padding` | `Optional[PaddingValue]` | `None` | Content padding |
| `width` | `Optional[Number]` | `None` | Fixed width (floating only) |
| `elevation` | `Optional[Number]` | `None` | Shadow elevation |
| `shape` | `Optional[OutlinedBorder]` | `None` | Shape |
| `clip_behavior` | `ClipBehavior` | `HARD_EDGE` | Content clipping |
| `on_action` | `Optional[ControlEventHandler[...]]` | `None` | Action clicked |
| `on_visible` | `Optional[ControlEventHandler[...]]` | `None` | First visible |

---

### DataTable

Data table with columns and rows.

| Property | Type | Default | Description |
|---|---|---|---|
| `columns` | `list[DataColumn]` | *(required)* | Column definitions |
| `rows` | `list[DataRow]` | `[]` | Row data definitions |
| `sort_ascending` | `bool` | `False` | Sort direction |
| `show_checkbox_column` | `bool` | `False` | Show row checkboxes |
| `sort_column_index` | `Optional[int]` | `None` | Primary sort column |
| `border` | `Optional[Border]` | `None` | Table border |
| `border_radius` | `Optional[BorderRadiusValue]` | `None` | Border corners |
| `horizontal_lines` | `Optional[BorderSide]` | `None` | Horizontal row lines |
| `vertical_lines` | `Optional[BorderSide]` | `None` | Vertical column lines |
| `column_spacing` | `Optional[Number]` | `None` | Column content spacing |
| `data_row_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Data row color by state |
| `data_row_min_height` | `Optional[Number]` | `None` | Min data row height |
| `data_row_max_height` | `Optional[Number]` | `None` | Max data row height |
| `data_text_style` | `Optional[TextStyle]` | `None` | Data text style |
| `bgcolor` | `Optional[ColorValue]` | `None` | Table background color |
| `divider_thickness` | `Number` | `1.0` | Row divider thickness |
| `heading_row_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Heading row color |
| `heading_row_height` | `Optional[Number]` | `None` | Heading row height |
| `heading_text_style` | `Optional[TextStyle]` | `None` | Heading text style |
| `horizontal_margin` | `Optional[Number]` | `None` | Edge horizontal margin |
| `clip_behavior` | `ClipBehavior` | `NONE` | Content clipping |
| `on_select_all` | `Optional[ControlEventHandler[...]]` | `None` | Select all rows |

### ListTile

A single fixed-height row (for lists).

| Property | Type | Default | Description |
|---|---|---|---|
| `title` | `Optional[StrOrControl]` | `None` | Primary content |
| `subtitle` | `Optional[StrOrControl]` | `None` | Content below title |
| `is_three_line` | `Optional[bool]` | `None` | Three-line layout |
| `leading` | `Optional[IconDataOrControl]` | `None` | Control before title |
| `trailing` | `Optional[IconDataOrControl]` | `None` | Control after title |
| `content_padding` | `Optional[PaddingValue]` | `None` | Internal padding |
| `bgcolor` | `Optional[ColorValue]` | `None` | Background color |
| `selected` | `bool` | `False` | Whether selected |
| `dense` | `Optional[bool]` | `None` | Dense/compact layout |
| `autofocus` | `bool` | `False` | Focus on creation |
| `toggle_inputs` | `bool` | `False` | Toggle child inputs on tap |
| `selected_color` | `Optional[ColorValue]` | `None` | Selected icon/text color |
| `selected_tile_color` | `Optional[ColorValue]` | `None` | Selected background |
| `icon_color` | `Optional[ColorValue]` | `None` | Default icon color |
| `text_color` | `Optional[ColorValue]` | `None` | Default text color |
| `shape` | `Optional[OutlinedBorder]` | `None` | Tile shape |
| `visual_density` | `Optional[VisualDensity]` | `None` | Layout compactness |
| `title_text_style` | `Optional[TextStyle]` | `None` | Title text style |
| `subtitle_text_style` | `Optional[TextStyle]` | `None` | Subtitle text style |
| `url` | `Optional[Union[str, Url]]` | `None` | URL to open on click |
| `on_click` | `Optional[ControlEventHandler[...]]` | `None` | Click handler |
| `on_long_press` | `Optional[ControlEventHandler[...]]` | `None` | Long press handler |

### ExpansionTile

Expandable/collapsible tile.

| Property | Type | Default | Description |
|---|---|---|---|
| `title` | `StrOrControl` | *(required)* | Primary heading |
| `controls` | `Optional[list[Control]]` | `None` | Expanded children |
| `subtitle` | `Optional[StrOrControl]` | `None` | Content below title |
| `leading` | `Optional[IconDataOrControl]` | `None` | Control before title |
| `trailing` | `Optional[IconDataOrControl]` | `None` | Control after title |
| `controls_padding` | `Optional[PaddingValue]` | `None` | Expanded content padding |
| `tile_padding` | `Optional[PaddingValue]` | `None` | Header padding |
| `expanded_alignment` | `Optional[Alignment]` | `None` | Expanded alignment |
| `expanded_cross_axis_alignment` | `CrossAxisAlignment` | `CENTER` | Horizontal alignment |
| `maintain_state` | `bool` | `False` | Keep children in tree |
| `text_color` | `Optional[ColorValue]` | `None` | Expanded title color |
| `icon_color` | `Optional[ColorValue]` | `None` | Expanded arrow color |
| `bgcolor` | `Optional[ColorValue]` | `None` | Expanded background |
| `collapsed_bgcolor` | `Optional[ColorValue]` | `None` | Collapsed background |
| `collapsed_icon_color` | `Optional[ColorValue]` | `None` | Collapsed arrow color |
| `collapsed_text_color` | `Optional[ColorValue]` | `None` | Collapsed title color |
| `shape` | `Optional[OutlinedBorder]` | `None` | Expanded border shape |
| `collapsed_shape` | `Optional[OutlinedBorder]` | `None` | Collapsed border shape |
| `dense` | `Optional[bool]` | `None` | Dense/compact layout |
| `expanded` | `bool` | `False` | Current expansion state |
| `visual_density` | `Optional[VisualDensity]` | `None` | Layout compactness |
| `on_change` | `Optional[ControlEventHandler[...]]` | `None` | Expansion toggled |

### Chip

Compact element representing an attribute, action, or filter.

| Property | Type | Default | Description |
|---|---|---|---|
| `label` | `StrOrControl` | *(required)* | Primary chip content |
| `leading` | `Optional[Control]` | `None` | Control left of label |
| `selected` | `bool` | `False` | Selection state |
| `selected_color` | `Optional[ColorValue]` | `None` | Selected background color |
| `elevation` | `Optional[Number]` | `None` | Shadow elevation |
| `bgcolor` | `Optional[ColorValue]` | `None` | Unselected background |
| `show_checkmark` | `bool` | `True` | Checkmark when selected |
| `check_color` | `Optional[ColorValue]` | `None` | Checkmark color |
| `shadow_color` | `Optional[ColorValue]` | `None` | Shadow color |
| `shape` | `Optional[OutlinedBorder]` | `None` | Border shape |
| `padding` | `Optional[PaddingValue]` | `None` | Label padding |
| `delete_icon` | `Optional[Control]` | `None` | Delete icon control |
| `delete_icon_color` | `Optional[ColorValue]` | `None` | Delete icon color |
| `label_padding` | `Optional[PaddingValue]` | `None` | Inner label padding |
| `label_text_style` | `Optional[TextStyle]` | `None` | Label style |
| `autofocus` | `bool` | `False` | Focus on creation |
| `clip_behavior` | `ClipBehavior` | `NONE` | Content clipping |
| `visual_density` | `Optional[VisualDensity]` | `None` | Layout compactness |
| `border_side` | `Optional[BorderSide]` | `None` | Outline border |
| `on_click` | `Optional[ControlEventHandler[...]]` | `None` | Chip clicked |
| `on_delete` | `Optional[ControlEventHandler[...]]` | `None` | Delete icon clicked |
| `on_select` | `Optional[ControlEventHandler[...]]` | `None` | Selection toggled |

---

### ProgressBar

Linear progress indicator.

| Property | Type | Default | Description |
|---|---|---|---|
| `value` | `Optional[Number]` | `None` | Progress 0.0–1.0 (`None` = indeterminate) |
| `bar_height` | `Optional[Number]` | `None` | Line height |
| `color` | `Optional[ColorValue]` | `None` | Indicator color |
| `bgcolor` | `Optional[ColorValue]` | `None` | Track color |
| `border_radius` | `Optional[BorderRadiusValue]` | `None` | Indicator/track radius |
| `semantics_label` | `Optional[str]` | `None` | Accessibility label |

### ProgressRing

Circular progress indicator.

| Property | Type | Default | Description |
|---|---|---|---|
| `value` | `Optional[Number]` | `None` | Progress 0.0–1.0 (`None` = indeterminate) |
| `stroke_width` | `Optional[Number]` | `None` | Circle line width |
| `color` | `Optional[ColorValue]` | `None` | Indicator color |
| `bgcolor` | `Optional[ColorValue]` | `None` | Track color |
| `stroke_align` | `Optional[Number]` | `None` | Stroke position (-1 to 1) |
| `stroke_cap` | `Optional[StrokeCap]` | `None` | Line ending style |
| `semantics_label` | `Optional[str]` | `None` | Accessibility label |

### Divider

Thin horizontal line.

| Property | Type | Default | Description |
|---|---|---|---|
| `color` | `Optional[ColorValue]` | `None` | Line color |
| `height` | `Optional[Number]` | `None` | Height extent (default 16) |
| `leading_indent` | `Optional[Number]` | `None` | Leading empty space |
| `thickness` | `Optional[Number]` | `None` | Line thickness |
| `trailing_indent` | `Optional[Number]` | `None` | Trailing empty space |

---

### SearchBar

Material 3 search bar with suggestions view.

| Property | Type | Default | Description |
|---|---|---|---|
| `controls` | `list[Control]` | `[]` | Suggestion controls |
| `value` | `str` | `""` | Search text value |
| `bar_leading` | `Optional[Control]` | `None` | Control before text (closed) |
| `bar_trailing` | `Optional[list[Control]]` | `None` | Controls after text (closed) |
| `bar_hint_text` | `Optional[str]` | `None` | Placeholder text (closed) |
| `bar_bgcolor` | `Optional[ControlStateValue[ColorValue]]` | `None` | Bar background by state |
| `bar_overlay_color` | `Optional[ControlStateValue[ColorValue]]` | `None` | Bar highlight by state |
| `bar_elevation` | `Optional[ControlStateValue[Optional[Number]]]` | `None` | Bar elevation by state |
| `bar_shape` | `Optional[ControlStateValue[OutlinedBorder]]` | `None` | Bar shape by state |
| `bar_text_style` | `Optional[ControlStateValue[TextStyle]]` | `None` | Bar text style by state |
| `view_leading` | `Optional[Control]` | `None` | Control before text (open) |
| `view_trailing` | `Optional[list[Control]]` | `None` | Controls after text (open) |
| `view_elevation` | `Optional[Number]` | `None` | View elevation |
| `view_bgcolor` | `Optional[ColorValue]` | `None` | View background color |
| `view_hint_text` | `Optional[str]` | `None` | View placeholder text |
| `view_shape` | `Optional[OutlinedBorder]` | `None` | View shape |
| `full_screen` | `bool` | `False` | Full-screen search view |
| `keyboard_type` | `KeyboardType` | `TEXT` | Keyboard input type |
| `autofocus` | `bool` | `False` | Auto-focus text field |
| `on_tap` | `Optional[ControlEventHandler[...]]` | `None` | Bar tapped |
| `on_submit` | `Optional[ControlEventHandler[...]]` | `None` | Enter pressed |
| `on_change` | `Optional[ControlEventHandler[...]]` | `None` | Text changed |
| `on_focus` | `Optional[ControlEventHandler[...]]` | `None` | Focus gained |
| `on_blur` | `Optional[ControlEventHandler[...]]` | `None` | Focus lost |

### GestureDetector

Detects gestures on a child control.

| Property | Type | Default | Description |
|---|---|---|---|
| `content` | `Optional[Control]` | `None` | Child control |
| `mouse_cursor` | `Optional[MouseCursor]` | `None` | Hover mouse cursor |
| `drag_interval` | `int` | `0` | Drag event throttle (ms) |
| `hover_interval` | `int` | `0` | Hover event throttle (ms) |
| `on_tap` | `Optional[EventHandler[...]]` | `None` | Primary tap |
| `on_tap_down` | `Optional[EventHandler[...]]` | `None` | Tap down |
| `on_tap_up` | `Optional[EventHandler[...]]` | `None` | Tap up |
| `on_secondary_tap` | `Optional[ControlEventHandler[...]]` | `None` | Secondary button tap |
| `on_long_press` | `Optional[ControlEventHandler[...]]` | `None` | Long press |
| `on_double_tap` | `Optional[ControlEventHandler[...]]` | `None` | Double tap |
| `on_horizontal_drag_start` | `Optional[EventHandler[...]]` | `None` | Horizontal drag started |
| `on_horizontal_drag_update` | `Optional[EventHandler[...]]` | `None` | Horizontal drag moved |
| `on_horizontal_drag_end` | `Optional[EventHandler[...]]` | `None` | Horizontal drag ended |
| `on_vertical_drag_start` | `Optional[EventHandler[...]]` | `None` | Vertical drag started |
| `on_vertical_drag_update` | `Optional[EventHandler[...]]` | `None` | Vertical drag moved |
| `on_vertical_drag_end` | `Optional[EventHandler[...]]` | `None` | Vertical drag ended |
| `on_pan_start` | `Optional[EventHandler[...]]` | `None` | Pan started |
| `on_pan_update` | `Optional[EventHandler[...]]` | `None` | Pan moved |
| `on_pan_end` | `Optional[EventHandler[...]]` | `None` | Pan ended |
| `on_scale_start` | `Optional[EventHandler[...]]` | `None` | Scale started |
| `on_scale_update` | `Optional[EventHandler[...]]` | `None` | Scale updated |
| `on_scale_end` | `Optional[EventHandler[...]]` | `None` | Scale ended |
| `on_hover` | `Optional[EventHandler[...]]` | `None` | Mouse pointer hovering |
| `on_enter` | `Optional[EventHandler[...]]` | `None` | Mouse entered |
| `on_exit` | `Optional[EventHandler[...]]` | `None` | Mouse exited |
| `on_scroll` | `Optional[EventHandler[...]]` | `None` | Scroll event |

---

## Links & Resources

- **Official Docs:** [docs.flet.dev](https://docs.flet.dev/)
- **GitHub:** [github.com/flet-dev/flet](https://github.com/flet-dev/flet)
- **PyPI:** [pypi.org/project/flet](https://pypi.org/project/flet/)
- **Tutorials:** [Calculator](https://docs.flet.dev/tutorials/calculator/), [Chat](https://docs.flet.dev/tutorials/chat/), [ToDo](https://docs.flet.dev/tutorials/todo/), [Solitaire](https://docs.flet.dev/tutorials/solitaire/)
- **Gallery:** [flet.dev/gallery](https://flet.dev/gallery)
- **Roadmap:** [flet.dev/roadmap](https://flet.dev/roadmap)
- **Discord:** [discord.gg/dzWXP8SHG8](https://discord.gg/dzWXP8SHG8)
- **Discussions:** [github.com/flet-dev/flet/discussions](https://github.com/flet-dev/flet/discussions)
- **Contributing:** [CONTRIBUTING.md](https://github.com/flet-dev/flet/blob/main/CONTRIBUTING.md)
