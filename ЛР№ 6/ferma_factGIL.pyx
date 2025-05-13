from libc.math cimport sqrt
from libc.math cimport ceil
from libc.stdlib cimport malloc, free
from cython cimport boundscheck, wraparound, nonecheck, cdivision

@boundscheck(False)
@wraparound(False)
@nonecheck(False)
@cdivision(True)
def fermat_factorization(unsigned long long N):
    cdef unsigned long long x, y, y_squared

    if N % 2 == 0:
        return (2, N // 2)

    x = <unsigned long long>ceil(sqrt(<double>N)) + 1

    with nogil:
        while True:
            y_squared = x * x - N
            y = <unsigned long long>sqrt(<double>y_squared)
            if y * y == y_squared:
                break
            x += 1

    return (x - y, x + y)
