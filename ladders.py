#!/usr/bin/env python
# -*- coding: utf-8 -*-

def ladder(N):
    """
    #m - memory
    """
    m = {}

    def f(n, b):
        """
        n - number of blocks
        b - ladder base
        """
        if n == b:
            return 1
        if b > n:
            return 0
        if n < 1 or b < 1:
            return 0
        if (n, b) in m:
            return m[(n, b)]
        #main dynamic
        #ladder base in childern from 1 to b - 1
        m[(n, b)] = sum(f(n - b, i) for i in xrange(1, b))
        return m[(n, b)]

    return sum(f(N, i) for i in xrange(1, N + 1))

number = int(raw_input())
print ladder(number)


