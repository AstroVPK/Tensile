import pdb


def func(x, y, **kwargs):
    z = x + y
    return z, None

def altfunc(x, y, **kwargs):
    z = x*y
    z1 = x + y
    z2 = x - y
    return z, (z1, z2)

x = 1
y = 2

test1, extras1 = func(x, y)

test2, extras2 = altfunc(x, y)

pdb.set_trace()