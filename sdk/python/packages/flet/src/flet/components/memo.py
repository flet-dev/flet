def memo(fn):
    fn.__is_memo__ = True
    impl = getattr(fn, "__component_impl__", None)
    if impl is not None:
        impl.__is_memo__ = True
    return fn
