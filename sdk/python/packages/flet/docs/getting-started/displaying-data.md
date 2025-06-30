## Text

`Text` control is used to output textual data. Its main properties are `value` and `size`, but it also has a number of formatting properties to control its appearance. For example:

```python
t = ft.Text(
    value="This is a Text control sample",
    size=30,
    color="white",
    bgcolor="pink",
    weight="bold",
    italic=True,
)
page.add(t)
```
<img src="/img/docs/getting-started/displaying-data-text.png" className="screenshot-50" />

### Text styles

[TBD]
Fonts?
Variable weight?
Built-in styles with customization.
TextField class description.



## Icon

* Icons list
* Link to an app

## Image

Note about CORS
Side-loading assets
HTML renderer in web to display all formats
what formats are supported?

in the desktop version it does support jpeg, jpg, png
in the web version it only supports png 
Could you try using html renderer for the web? https://flet.dev/docs/controls/text/#using-system-fonts
Reading this I think "html" renderer must support any format supported by the browser: https://docs.flutter.dev/development/platform-integration/web/web-images