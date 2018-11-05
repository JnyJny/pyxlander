'''
'''


def will_wrap(value, lo, hi):
    return value < lo or value > hi

def wrap(value, lo, hi):
    if value > hi:
        return lo
    if value < lo:
        return hi
    return value

def constrain(value, lo, hi):
    return min(hi, max(lo, value))

def wrapxy(x, y, w, h, ox=0, oy=0, randomize_on_wrap=False):

    if randomize_on_wrap:
        if will_wrap(x, ox, w):
            pass
        if will_wrap(y, oy, h):
            pass

    return wrap(x, ox, w), wrap(y, oy, h)

        
            
        
