from functools import reduce
from toolz import pipe

def pi(f, start, stop):
    
    numbers = [f(x) for x in range(start, stop + 1)] 
    result = reduce(lambda a, b: a*b, numbers)

    return(result)

def sigma(f, start, stop):

    numbers = [f(x) for x in range(start, stop + 1)] 
    result = reduce(lambda a, b: a+b, numbers)

    return(result)
