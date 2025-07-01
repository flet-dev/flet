::: flet.TextField

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/textfield)

### Basic TextFields



```python
import flet as ft

def main(page: ft.Page):
    def button_clicked(e):
        t.value = f"Textboxes values are:  '{tb1.value}', '{tb2.value}', '{tb3.value}', '{tb4.value}', '{tb5.value}'."
        page.update()

    t = ft.Text()
    tb1 = ft.TextField(label="Standard")
    tb2 = ft.TextField(label="Disabled", disabled=True, value="First name")
    tb3 = ft.TextField(label="Read-only", read_only=True, value="Last name")
    tb4 = ft.TextField(label="With placeholder", hint_text="Please enter text here")
    tb5 = ft.TextField(label="With an icon", icon=ft.Icons.EMOJI_EMOTIONS)
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(tb1, tb2, tb3, tb4, tb5, b, t)

ft.run(main)
```


<img src="/img/docs/controls/textfield/basic-textfield.gif" className="screenshot-40"/>

### TextField with `on_change` event



```python
import flet as ft

def main(page: ft.Page):
    def textbox_changed(e):
        t.value = e.control.value
        page.update()

    t = ft.Text()
    tb = ft.TextField(
        label="Textbox with 'change' event:",
        on_change=textbox_changed,
    )

    page.add(tb, t)

ft.run(main)
```


<img src="/img/docs/controls/textfield/textfield-with-change-event.gif" className="screenshot-40"/>

### Password with reveal button



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.TextField(
            label="Password with reveal button", password=True, can_reveal_password=True
        )
    )

ft.run(main)
```


<img src="/img/docs/controls/textfield/textfield-with-password.gif" className="screenshot-40"/>

### Multiline TextFields



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.TextField(label="standard", multiline=True),
        ft.TextField(
            label="disabled",
            multiline=True,
            disabled=True,
            value="line1\nline2\nline3\nline4\nline5",
        ),
        ft.TextField(
            label="Auto adjusted height with max lines",
            multiline=True,
            min_lines=1,
            max_lines=3,
        ),
    )

ft.run(main)
```


<img src="/img/docs/controls/textfield/textfield-with-multiline.gif" className="screenshot-40"/>

### Underlined and borderless TextFields



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.TextField(label="Underlined", border="underline", hint_text="Enter text here"),
        ft.TextField(
            label="Underlined filled",
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            hint_text="Enter text here",
        ),
        ft.TextField(label="Borderless", border="none", hint_text="Enter text here"),
        ft.TextField(
            label="Borderless filled",
            border=ft.InputBorder.NONE,
            filled=True,
            hint_text="Enter text here",
        ),
    )

ft.run(main)
```


<img src="/img/docs/controls/textfield/textfield-with-underline-and-borderless.gif" className="screenshot-40"/>

### TextFields with prefixes and suffixes



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.TextField(label="With prefix", prefix_text="https://"),
        ft.TextField(label="With suffix", suffix_text=".com"),
        ft.TextField(
            label="With prefix and suffix", prefix_text="https://", suffix_text=".com"
        ),
        ft.TextField(
            label="My favorite color",
            icon=ft.Icons.FORMAT_SIZE,
            hint_text="Type your favorite color",
            helper_text="You can type only one color",
            counter_text="0 symbols typed",
            prefix_icon=ft.Icons.COLOR_LENS,
            suffix_text="...is your color",
        ),
    )

ft.run(main)
```


<img src="/img/docs/controls/textfield/textfield-with-prefix-and-suffix.gif" className="screenshot-40"/>

