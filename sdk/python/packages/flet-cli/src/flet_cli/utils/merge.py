def merge_dict(a: dict, b: dict, path=[]):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dict(a[key], b[key], path + [str(key)])
            elif a[key] != b[key]:
                raise Exception(
                    "Cannot merge {}: {} and {}".format(
                        ".".join(path + [str(key)]), a[key], b[key]
                    )
                )
        else:
            a[key] = b[key]
    return a
