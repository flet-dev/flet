{{ class_all_options("flet.InputFilter") }}

## Predefined filters

{{ class_all_options("flet.NumbersOnlyInputFilter", show_root_heading=True) }}
{{ class_all_options("flet.TextOnlyInputFilter", show_root_heading=True) }}

## Usage example

```python
ft.CupertinoTextField(
    placeholder_text="Only numbers are allowed",
    input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
)
```

```python
ft.TextField(
    label="Only letters are allowed",
    input_filter=ft.TextOnlyInputFilter()
)
```
