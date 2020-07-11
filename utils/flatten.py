def flattenClass(inp):
    inp = inp.__dict__
    for key in inp.keys():
        if not type(inp[key]) in [int, dict, str, float, bool, type(None)]:
            inp[key] = flattenClass(inp[key])
    return inp
