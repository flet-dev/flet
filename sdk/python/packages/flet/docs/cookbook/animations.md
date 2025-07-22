## Implicit animations

With implicit animations, you can animate a control property by setting a target value; whenever that target
value changes, the control animates the property from the old value to the new one.

Animation produces interpolated values between the old and the new value over the given *duration*.

By default, the animation is *linearly* increasing the animation value, however, a *curve* can be
applied to the animation which changes the value according to the provided curve.
For example, `AnimationCurve.EASE_OUT_CUBIC` curve increases the animation value quickly at the
beginning of the animation and then slows down until the target value is reached:

<video controls>
  <source src="https://flutter.github.io/assets-for-api-docs/assets/animation/curve_ease_out_cubic.mp4"/>
</video>
/// caption
///

[`ConstrainedControl`][flet.ConstrainedControl] (and its subclasses) provides a number of `animate_{something}`
properties, described below, to enable implicit animation of its appearance:

* `animate_opacity`
* `animate_rotation`
* `animate_scale`
* `animate_offset`
* `animate_position`
* `animate` (`Container`)

`animate_*` properties could have one of the following values:

* Instance of [`Animation`][flet.Animation] - allows configuring the duration and the curve of the
* animation, for example `animate_rotation=Animation(duration=300, curve=AnimationCurve.BOUNCE_OUT)`.
  See [this](https://api.flutter.dev/flutter/animation/Curves-class.html) Flutter docs on animation curves for possible values. Default is `linear`.
* `int` value - enables animation with specified duration in milliseconds and `linear` curve.
* `bool` value - enables animation with the duration of 1000 milliseconds and `linear` curve.


```python
--8<-- "https://raw.githubusercontent.com/flet-dev/flet/refs/heads/docs/sdk/python/examples/python/controls/time-picker/basic.py"
```

![basic](https://raw.githubusercontent.com/flet-dev/flet/docs/sdk/python/examples/python/controls/time-picker/media/basic.png){width="80%"}
/// caption
///




### Opacity animation

Setting control's `animate_opacity` to either `True`, number or an instance of `Animation` class (see above)
enables implicit animation of [`ConstrainedControl.opacity`][flet.ConstrainedControl.opacity] property.

```python
--8<-- "https://raw.githubusercontent.com/flet-dev/flet/refs/heads/docs/sdk/python/examples/python/controls/constrained-control/animate-opacity.py"
```

![animate-opacity](https://raw.githubusercontent.com/flet-dev/flet/docs/sdk/python/examples/python/controls/constrained-control/media/animate-opacity.gif){width="80%"}
/// caption
///

### Rotation animation

Setting control's `animate_rotation` to either `True`, number or an instance of `Animation` class (see above)
enables implicit animation of [`ConstrainedControl.rotate`][flet.ConstrainedControl.rotate] property.

```python
--8<-- "https://raw.githubusercontent.com/flet-dev/flet/refs/heads/docs/sdk/python/examples/python/controls/constrained-control/animate-rotation.py"
```

![animate-rotation](https://raw.githubusercontent.com/flet-dev/flet/docs/sdk/python/examples/python/controls/constrained-control/media/animate-rotation.gif){width="80%"}
/// caption
///

### Scale animation

Setting control's `animate_scale` to either `True`, number or an instance of `Animation` class (see above)
enables implicit animation of [`ConstrainedControl.scale`][flet.ConstrainedControl.scale] property.

```python
--8<-- "https://raw.githubusercontent.com/flet-dev/flet/refs/heads/docs/sdk/python/examples/python/controls/constrained-control/animate-scale.py"
```

![animate-scale](https://raw.githubusercontent.com/flet-dev/flet/docs/sdk/python/examples/python/controls/constrained-control/media/animate-scale.gif){width="80%"}
/// caption
///

### Offset animation

Setting control's `animate_offset` to either `True`, number or an instance of `Animation` class (see above)
enables implicit animation of [`ConstrainedControl.offset`][flet.ConstrainedControl.offset] property.

`offset` property is an instance of `Offset` class which specifies horizontal `x` and vertical `y`
offset of a control scaled to control's size. For example, an offset `Offset(-0.25, 0)` will result in
a horizontal translation of one quarter the width of the control.

Offset animation is used for various sliding effects:

```python
--8<-- "https://raw.githubusercontent.com/flet-dev/flet/refs/heads/docs/sdk/python/examples/python/controls/constrained-control/animate-offset.py"
```

![animate-offset](https://raw.githubusercontent.com/flet-dev/flet/docs/sdk/python/examples/python/controls/constrained-control/media/animate-offset.gif){width="80%"}
/// caption
///

### Position animation

Setting control's `animate_position` to either `True`, number or an instance of `Animation` class
(see above) enables implicit animation of the following `ConstrainedControl` properties:
[`left`][flet.ConstrainedControl.left], [`right`][flet.ConstrainedControl.right],
[`bottom`][flet.ConstrainedControl.bottom], [`top`][flet.ConstrainedControl.top].


Note:
    Positioning is effective only if the control is a descendant of one of the following:

    - [`Stack`][flet.Stack] control
    - [`Page.overlay`][flet.Page.overlay] list

```python
--8<-- "https://raw.githubusercontent.com/flet-dev/flet/refs/heads/docs/sdk/python/examples/python/controls/constrained-control/animate-position.py"
```

![animate-position](https://raw.githubusercontent.com/flet-dev/flet/docs/sdk/python/examples/python/controls/constrained-control/media/animate-position.gif){width="80%"}
/// caption
///

### Animate

Setting [`Container.animate`][flet.Container.animate] to [`AnimationValue`][flet.AnimationValue]
enables implicit animation of container properties such as size, background color, border style, gradient.

```python
--8<-- "https://raw.githubusercontent.com/flet-dev/flet/refs/heads/docs/sdk/python/examples/python/controls/container/animate.py"
```

![animate](https://raw.githubusercontent.com/flet-dev/flet/docs/sdk/python/examples/python/controls/container/media/animate.gif){width="80%"}


### Animated content switcher

[`AnimatedSwitcher`][flet.AnimatedSwitcher] allows animated transition between a new control and
the control previously set on the `AnimatedSwitcher` as a `content`.

```python
import time

import flet as ft

def main(page: ft.Page):
    i = ft.Image(src="https://picsum.photos/150/150", width=150, height=150)

    def animate(e):
        sw.content = ft.Image(
            src=f"https://picsum.photos/150/150?{time.time()}", width=150, height=150
        )
        page.update()

    sw = ft.AnimatedSwitcher(
        i,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=500,
        reverse_duration=500,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
    )

    page.add(
        sw,
        ft.ElevatedButton("Animate!", on_click=animate),
    )

ft.run(main)
```

![animated-switcher](../assets/cookbook/animations/animated-switcher.gif){width="80%"}
/// caption
///

### Animation end callback

[`ConstrainedControl`][flet.ConstrainedControl] also has an
[`on_animation_end`][flet.ConstrainedControl.on_animation_end] event handler, which is called
when an animation is complete. It can be used to chain multiple animations.

Event's [`data`][flet.Event.data] field/property contains the name of animation:

* `"opacity"`
* `"rotation"`
* `"scale"`
* `"offset"`
* `"position"`
* `"container"`

For example:

```python
ft.Container(
    content=ft.Text("Animate me!"),
    animate=ft.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
    on_animation_end=lambda e: print("Container animation end:", e.data)
)
```
