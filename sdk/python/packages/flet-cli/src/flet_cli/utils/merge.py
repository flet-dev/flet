def merge_dict(a: dict, b: dict, path=[]):
    for key in b:
        if key in a and isinstance(a[key], dict) and isinstance(b[key], dict):
            merge_dict(a[key], b[key], path + [str(key)])
        else:
            a[key] = b[key]
    return a
