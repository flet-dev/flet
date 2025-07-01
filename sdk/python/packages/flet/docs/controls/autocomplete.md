::: flet.AutoComplete

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/autocomplete)

### Basic example



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.AutoComplete(
            suggestions=[
                ft.AutoCompleteSuggestion(key="one 1", value="One"),
                ft.AutoCompleteSuggestion(key="two 2", value="Two"),
                ft.AutoCompleteSuggestion(key="three 3", value="Three"),
            ],
            on_select=lambda e: print(e.control.selected_index, e.selection),
        )
    )

ft.run(main)
```


<img src="/img/docs/controls/autocomplete/autocomplete-example.gif" className="screenshot-40"/>

