from math import sqrt

def dot_product(v1, v2):
    net_sum = 0
    for i, _ in enumerate(v1):
        net_sum += v1[i]*v2[i]
    return net_sum

def tuple_sum(t1, t2):
    return tuple(map(sum, zip(t1,t2)))

def norm(v):
    norm = 0
    for element in v:
        norm += element**2
    norm = sqrt(norm)
    return norm