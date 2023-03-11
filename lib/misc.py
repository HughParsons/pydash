from inspect import signature
def parameters(func):
    return signature(func).parameters