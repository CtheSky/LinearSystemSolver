def clip(v, vmax, vmin):
    if v > vmax:
        return vmax
    if v < vmin:
        return vmin
    return v
