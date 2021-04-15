from math import log10 as lg


def db(val):
    return 10 ** (val / 20)


def rel(val, peak, digs=0):
    if val == 0:
        return '-inf'
    return str(round(20 * lg(abs(val) / peak), digs))
