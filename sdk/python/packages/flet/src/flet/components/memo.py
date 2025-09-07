from flet.components.component import _get_renderer


def memo(fn):
    def memo_wrapper(*args, **kwargs):
        r = _get_renderer()
        r.set_memo()
        return fn(*args, **kwargs)

    return memo_wrapper
