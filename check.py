from glob import glob


a=5
def f():
    global a
    a+=6
    return a
f()