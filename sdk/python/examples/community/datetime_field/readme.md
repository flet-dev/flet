# Calendar Input For Flet
## The calendar feature was not available in the Flet library of Python, so I wrote a small code for it.

You can review the code and add it to your own code in the form of `ft.Row`.
I also calculated the number of days in each month that vary.

![flet-calendar](https://i.ibb.co/5k4DqQp/Screenshot-2022-12-21-at-16-27-33.png)

# Using
```python
import flet as ft
from flet.datetime_field import DatetimeField

callback = lambda e : print(e)
def main(page: ft.Page):
    calendar = DatetimeField(page=page,
                             on_change=callback)
    page.add(calendar)

ft.app(target=main)
```

callback is on_change function, page is flets page.

### Output

```
['2020', None, None, None, None]
['2020', 'March', None, None, None]
['2020', 'April', None, None, None]
['2020', 'April', '4', None, None]
['2020', 'April', '4', '3', None]
2020-04-04 03:03:00
```

If values contains None, return a list, else return datetime
