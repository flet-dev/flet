from flet.components.utils import current_renderer


def memo(fn):
    def memo_wrapper(*args, **kwargs):
        r = current_renderer()
        r.set_memo()
        return fn(*args, **kwargs)

    return memo_wrapper
