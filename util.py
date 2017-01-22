from decimal import Decimal


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


def clip(v, vmax, vmin):
    if v > vmax:
        return vmax
    if v < vmin:
        return vmin
    return v
