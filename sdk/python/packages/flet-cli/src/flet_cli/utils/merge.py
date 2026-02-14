def merge_dict(a: dict, b: dict, path=[]):
    """
    Recursively merge dictionary `b` into dictionary `a`.

    For keys present in both dictionaries:
    - if both values are dictionaries, they are merged recursively;
    - otherwise, the value from `b` replaces the value in `a`.

    Args:
        a: Destination dictionary that is updated in place.
        b: Source dictionary whose values are merged into `a`.
        path: Internal recursion path used while descending nested dictionaries.

    Returns:
        The updated destination dictionary `a`.
    """

    for key in b:
        if key in a and isinstance(a[key], dict) and isinstance(b[key], dict):
            merge_dict(a[key], b[key], path + [str(key)])
        else:
            a[key] = b[key]
    return a
