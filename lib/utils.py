import functools as fntools

def pipe(*functions):
    def inner(x):
        for function in functions:
            x = function(x)
        return x
    return inner

def flow(x, functions):
    return pipe(*functions)(x)
