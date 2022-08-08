# Copyright (c) 2022 kamyu. All rights reserved.
#
# Google Code Jam 2022 Virtual World Finals - Problem E. Triangles
# https://codingcompetitions.withgoogle.com/codejam/round/000000000087762e/0000000000b9c555
#
# Time:  O(N^2), only pass in small set, both PyPy3 and Python3 TLE in large set (execution time of PyPy3 is about 18 seconds, and the time limit is 15 seconds, which is really tight)
# Space: O(N)
#

from math import gcd, atan2, pi

def vector(a, b):
    return [a[0]-b[0], a[1]-b[1]]

def inner_product(a, b):
    return a[0] * b[0] + a[1] * b[1]

def outer_product(a, b):
    return a[0] * b[1] - a[1] * b[0]

def ccw(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

# Return true if t is strictly inside a, b line segment
def is_strictly_inside_segment(t, a, b):
    return ccw(t, a, b) == 0 and inner_product(vector(a, t), vector(t, b)) > 0

# Return true if t is strictly inside a, b, c triangle
def is_stricly_inside_triangle(t, a, b, c):
    d1, d2, d3 = ccw(t, a, b),  ccw(t, b, c),  ccw(t, c, a)
    return (d1 > 0 and d2 > 0 and d3 > 0) or (d1 < 0 and d2 < 0 and d3 < 0)

# Return true if t is inside a, b, c triangle
def is_inside_triangle(t, a, b, c):
    d1, d2, d3 = ccw(t, a, b),  ccw(t, b, c),  ccw(t, c, a)
    return (d1 >= 0 and d2 >= 0 and d3 >= 0) or (d1 <= 0 and d2 <= 0 and d3 <= 0)

def cross(A, B, C, D):
    return ccw(A,C,D) * ccw(B,C,D) < 0 and ccw(A,B,C) * ccw(A,B,D) < 0

def angle(a, b):
    result = atan2(outer_product(a, b), inner_product(a, b))
    if result < 0:
        result += 2*pi
    return result

def line(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    # (x-x1)/(x2-x1) = (y-y1)/(y2-y1)
    # => (y2-y1)x - (x2-x1)y = x1(y2-y1) - y1(x2-x1)
    a, b, c = (y2-y1), -(x2-x1), x1*(y2-y1)-y1*(x2-x1)
    g = gcd(gcd(a, b), c)
    a, b, c = a//g, b//g, c//g
    return a, b, c

def insort(P, sorted_remain, x):
    sorted_remain.insert(next((i for i, y in enumerate(sorted_remain) if P[y] > P[x]), len(sorted_remain)), x)

def remove_unused(P, sorted_remain, C, l, result):
    a, b, c = l
    cnt = sum(a*x+b*y == c for x, y in P)
    remove_cnt = max(cnt-2*(len(P)-cnt), 0)
    while len(C) < remove_cnt:
        for i in result.pop():
            insort(P, sorted_remain, i)
            x, y = P[i]
            if a*x+b*y == c:
                C.add(i)
    for _ in range(remove_cnt):
        sorted_remain.remove(C.pop())

def find_nearest_point(P, sorted_remain, x, y):
    a1, d1, z1 = float("inf"), float("inf"), -1
    a2, d2, z2 = float("-inf"), float("inf"), -1
    for c in sorted_remain:
        a = angle(vector(P[y], P[x]), vector(P[y], P[c]))
        if a == 0.0 or a == pi:
            continue
        v = vector(P[y], P[c])
        d = inner_product(v, v)
        if a < pi:
            if a+EPS < a1:
                a1, d1, z1 = a, d, c
            elif a-EPS <= a1:
                if d < d1:
                    d1, z1 = d, c
        else:
            if a-EPS > a2:
                a2, d2, z2 = a, d, c
            elif a+EPS >= a2:
                if d < d2:
                    d2, z2 = d, c
    return z1 if z1 != -1 else z2

def make_triangle_from_maximal_points(P, sorted_remain, result):
    x, y = sorted_remain[-1], sorted_remain[-2]
    z = find_nearest_point(P, sorted_remain, x, y)
    if z == -1:
        return False
    result.append((x, y, z))
    for i in result[-1]:
        sorted_remain.remove(i)
    return True

def make_triangles_from_max_colinear(P, sorted_remain, C, result):
    other, colinear = [], []
    for x in sorted_remain:
        if x not in C:
            other.append(x)
        else:
            colinear.append(x)
    assert(len(colinear) <= 2*len(other))
    for _ in range(len(colinear)//2):
        x, y = colinear.pop(), colinear.pop()
        z = find_nearest_point(P, other, x, y)
        other.remove(z)
        result.append((x, y, z))
        for i in result[-1]:
            sorted_remain.remove(i)

def check(x, y, z, a, b, c):
    if (sum(is_stricly_inside_triangle(t, a, b, c) for t in (x, y, z)) == 1 and
        sum(not is_inside_triangle(t, a, b, c) for t in (x, y, z)) == 2) or \
       (sum(is_stricly_inside_triangle(t, x, y, z) for t in (a, b, c)) == 1 and
        sum(not is_inside_triangle(t, x, y, z) for t in (a, b, c)) == 2):
        return False
    for A, B in ((x, y), (y, z), (z, x)):
        for C, D in ((a, b), (b, c), (c, a)):
             if cross(A, B, C, D) or (ccw(A, C, D) == ccw(B, C, D) == 0 and
                (is_strictly_inside_segment(A, C, D) or is_strictly_inside_segment(B, C, D) or
                 is_strictly_inside_segment(C, A, B) or is_strictly_inside_segment(D, A, B))):
                return False
    return True

def make_triangles_by_brute_forces(P, sorted_remain, result):
    assert(len(sorted_remain) == 6)
    for i in range(len(sorted_remain)):
        for j in range(i+1, len(sorted_remain)):
            for k in range(j+1, len(sorted_remain)):
                x, y, z = sorted_remain[i], sorted_remain[j], sorted_remain[k]
                if not ccw(P[x], P[y], P[z]):
                    continue
                a, b, c = [o for o in sorted_remain if o not in [x, y, z]]
                if not ccw(P[a], P[b], P[c]) or not check(P[x], P[y], P[z], P[a], P[b], P[c]):
                    continue
                result.append((x, y, z))
                for i in result[-1]:
                    sorted_remain.remove(i)
                result.append((a, b, c))
                for i in result[-1]:
                    sorted_remain.remove(i)
                return
    assert(False)

def triangles():
    N = int(input())
    P = [list(map(int, input().split())) for _ in range(N)]
    result = []
    removed = False
    sorted_remain = sorted(range(N), key=lambda x: P[x])
    while len(sorted_remain) >= 3:
        if make_triangle_from_maximal_points(P, sorted_remain, result):
            continue
        i, j = sorted_remain[:2]
        a, b, c = line(P[i], P[j])
        C = set(sorted_remain)
        if not removed:
            removed = True
            remove_unused(P, sorted_remain, C, (a, b, c), result)
        while not len(C) <= 2*(len(sorted_remain)-len(C)):
            for i in result.pop():
                insort(P, sorted_remain, i)
                x, y = P[i]
                if a*x+b*y == c:
                    C.add(i)
        if len(C) == 3 and len(sorted_remain)//3 == 2:
            make_triangles_by_brute_forces(P, sorted_remain, result)
            continue
        make_triangles_from_max_colinear(P, sorted_remain, C, result)
    return "%s\n%s" % (len(result), "\n".join(map(lambda x: " ".join(map(lambda y: str(y+1), x)), result))) if result else 0

EPS = 1e-15
for case in range(int(input())):
    print('Case #%d: %s' % (case+1, triangles()))
