

def derivative(function, dx=10**-9):
    return lambda x: (function(x + dx) - function(x)) / dx

def newtons_method(f, x=0, y=0, n=10):
    f_prime = derivative(f)
    for _ in range(n):
        x = (y - f(x))/f_prime(x) + x
    return x