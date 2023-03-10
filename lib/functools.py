import functools as fn
from .misc import parameters as pars

def after(n, func):
    """
    Creates a function that invokes func once it's called n or more times.
    """
    encapsulated = {
        "call_count": 0,
    }
    
    def inner(*args):
        encapsulated["call_count"] += 1
        if encapsulated["call_count"] < n:
            return

        return func(*args)
    return inner

def ary(func, n):
    """
    Creates a function that accepts up to n arguments, ignoring any additional arguments.
    """
    def inner(*args):
        return func(*args[:n])
    return inner

def before(n, func):
    """
    Creates a function that invokes func up to n times (exclusive),
    any m >= n calls will return the result of the n-1th call.
    """
    encapsulated = {
        "call_count": 0,
        "last_result": None
    }

    def inner(*args):
        encapsulated["call_count"] += 1

        if encapsulated["call_count"] >= n:
            return encapsulated["last_result"]
        
        encapsulated["last_result"] = func(*args)
        return encapsulated["last_result"]

    return inner

def bind(func, instance, *partials):
    """
    Binds an instance to a function such that the function
    can access that instances variables as self.

    the functions first argument must be the reference to the instance.
    """
    args = [instance, *partials]
    def inner(*inner_args):
        return func(*args, *inner_args)
    return inner

def attach(func, instance, as_name=None):
    """
    Attaches a function to an instance such that the function can
    be accessed of the instance as a member.

    c: https://stackoverflow.com/questions/1015307/python-bind-an-unbound-method
    """

    if as_name is None:
        as_name = func.__name__
    bound_method = func.__get__(instance, instance.__class__)
    setattr(instance, as_name, bound_method)

    return bound_method

def curry(func, *args):
    """
    creates a function that accepts arguments partially until the number of 
    supplied arguments matches the arity of the function.
    """
    arg_len = len(pars(func))

    def inner(*inner_args):
        if len(inner_args) < arg_len:
            return curry(func, *inner_args)

        return func(*inner_args[:arg_len])
    return partial(inner, *args)

def curryRight(func, *args):
    arg_len = len(pars(func))
    
    def inner(*inner_args):
        if len(inner_args) < arg_len:
            return curry(func, *inner_args)

        return func(*inner_args[arg_len-1::-1])
    return partial(inner, *args)

# def debounce(func, wait=0, **kwargs):
#     pass

# def defer(func, *args):
#     pass

# def delay(func, wait, *args):
#     pass

# def flip(func):
#     pass

# def memoize(func):
#     pass

def negate(func):
    """
    returns a function that returns the logical negation 
    of the result of the supplied function
    """
    def inner(*args):
        return not func(*args)
    return inner

def once(func):
    return before(2, func)

def overArgs(func, transforms):
    arg_len = len(pars(func))

    if arg_len != len(transforms):
        print(arg_len, len(transforms))
        raise TypeError("the length of the supplied transforms does not match the arity of the function")

    def inner(*args):
        new_args = (transform(arg) for transform, arg in zip(transforms, args))
        return func(*new_args)
    return inner

def partial(func, /, *args, **kwargs):
    return fn.partial(func, *args, **kwargs)


def partialRight(func, /, *args, **kwargs):
    def inner(*inner_args, **inner_kwargs):
        return func(*inner_args, *args, **inner_kwargs, **kwargs)
    return inner

def rearg(func, indices):
    def inner(*args):
        rearanged_args = (args[idx] for idx in indices)
        return func(*rearanged_args)
    return inner

def rest(func, start=None):
    arg_len = len(pars(func))
    if start is None:
        start = arg_len - 1

    def inner(*args):
        non_rest_args = args[:start]
        rest_args = args[start:]
        return func(*non_rest_args, rest_args)

    return inner


def spread(func):
    """
    Essentially the inverse of rest, it takes a function of arity n 
    and returns a function of arity 1
    """
    def inner(args): # no iterable unpacking
        return func(*args)
    return inner

# def throttle(func, wait=0, **kwargs):
#     pass

def unary(func):
    return ary(func, 1)

def wrap(value, func):
    def inner(*args):
        return func(value, *args)
    return inner
