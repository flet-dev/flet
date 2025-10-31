from flet.components.utils import current_renderer


def memo(fn):
    """
    Lets you skip re-rendering a component when its props are unchanged.

    Example:
        ```python
        import flet as ft


        @ft.component
        def MyComponent(x, y):
            return ft.Text(f"x={x}, y={y}")


        MemoizedMyComponent = ft.memo(MyComponent)

        flet.run(
            lambda page: page.render(
                lambda: MemoizedMyComponent(x=1, y=2),
            ),
        )
        ```
    """

    def memo_wrapper(*args, **kwargs):
        r = current_renderer()
        r.set_memo()
        return fn(*args, **kwargs)

    return memo_wrapper
