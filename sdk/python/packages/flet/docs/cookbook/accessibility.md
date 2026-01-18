Flet is based on [Flutter](https://flutter.dev) which includes first-class framework support for
accessibility in addition to that provided by the underlying operating system.

## Screen readers

For mobile, screen readers ([TalkBack](https://support.google.com/accessibility/android/answer/6283677?hl=en), [VoiceOver](https://www.apple.com/lae/accessibility/iphone/vision/)) enable visually
impaired users to get spoken feedback about the contents of the screen and interact
with the UI via gestures on mobile and keyboard shortcuts on desktop.
Turn on VoiceOver or TalkBack on your mobile device and navigate around your app.

For web, the following screen readers are currently supported:

Mobile Browsers:

* iOS - VoiceOver
* Android - TalkBack

Desktop Browsers:

* MacOS - VoiceOver
* Windows - JAWs & NVDA

Screen Readers users on web will need to toggle "Enable accessibility"
button to build the semantics tree.

### Text

Use `Text.semantics_label` property to override default Text control semantics.

### Buttons

All buttons with text on them generate proper semantics.

Use `tooltip` property to add screen reader semantics for
[`IconButton`][flet.IconButton], [`FloatingActionButton`][flet.FloatingActionButton]
and [`PopupMenuButton`][flet.PopupMenuButton] buttons.

### `TextField` and `Dropdown`

Use `TextField.label` and `Dropdown.label` properties to add screen
reader semantics to those controls.

### Custom semantics

For any specific requirements use [`Semantics`][flet.Semantics] control.

### Debugging semantics

Set [`Page.show_semantics_debugger`][flet.Page.show_semantics_debugger] to `True`
to show an overlay that shows the accessibility information reported by the framework.

You can implement a specific [keyboard shortcut](keyboard-shortcuts.md) to conveniently toggle
semantics debugger during app development:

{{ image("../assets/cookbook/accessibility/debug-accessibility-toggle.gif", width="80%") }}

```python
--8<-- "../../examples/controls/page/semantics_debugger.py"
```
