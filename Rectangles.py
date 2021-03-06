#!/usr/bin/env python
# -*- coding: utf-8 -*-
#http://informatics.mccme.ru//mod/statements/view3.php?chapterid=644#1
import sys
import re
import time

x1, y1, x2, y2 = range(4)

def is_intersected(r1, r2):
    return r2[x1] < r1[x2] and r2[y1] < r1[y2] and \
           r2[x2] > r1[x1] and r2[y2] > r1[y1]

def is_absorbing(r1, r2):
    return r1[x1] <= r2[x1] and r1[y1] <= r2[y1] and \
           r1[x2] >= r2[x2] and r1[y2] >= r2[y2]

def calc_intersection(r1, r2):
    r = [0, 0, 0, 0]
    r[x1] = max(r1[x1], r2[x1])
    r[y1] = max(r1[y1], r2[y1])
    r[x2] = min(r1[x2], r2[x2])
    r[y2] = min(r1[y2], r2[y2])
    return tuple(r)

def calc_area(r):
    width = r[x2] - r[x1]
    height = r[y2] - r[y1]
    return  width * height

def calc_total_area(rects):
    n = len(rects)
    if n == 0:
        return 0
    if n == 1:
        return calc_area(rects[0])

    intr_area, rects = calc_intr_area(rects)
    raw_area = sum(map(calc_area, rects))

    return raw_area - intr_area

def calc_intr_area(rects):
    n = len(rects)
    intrs_area = 0#intersections area
    rects = sorted(rects, key=lambda rect: rect[y1])#to do zoning in at least one axis

    for r1_id in xrange(n - 1):
        r1 = rects[r1_id]
        if r1 is None:
            continue
        intersections = []
        for r2_id in xrange(r1_id + 1, n):
            r2 = rects[r2_id]

            if r2 is None:
                continue
            if r1[y2] < r2[y1]:#zoning
                break
            if not is_intersected(r1, r2):
                continue
            #absorbing allows to remove duplicates
            if is_absorbing(r1, r2):
                # r1 absorbs r2. All intersections of r2 will be in r1 so we in effect remove r2 from future consideration
                rects[r2_id] = None
                continue
            if is_absorbing(r2, r1):
                # r2 absorbs r1. All intersections of r1 will be in r2 as well so terminate earlier
                rects[r1_id] = None
                intersections = []
                break

            intersections.append(calc_intersection(r1, r2))

        intrs_area += calc_total_area(intersections)
    #remove absorbed rectangles
    pure_rects = filter(lambda rect: rect is not None, rects)
    return intrs_area, pure_rects

def process_input(input):
    raw_numbers = re.compile('\s+').split(input.strip())
    numbers = map(int, raw_numbers)
    num_rects, raw_rects = numbers[0], numbers[1:]
    rects = []
    for i in xrange(num_rects):
        #rects - 4 numbers per line
        rect = tuple(raw_rects[(i * 4):(i * 4 + 4)])
        x1, y1, x2, y2 = rect
        #to inforce left-bottom, right-top notation
        x1, y1, x2, y2 = min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
        rect = (x1, y1, x2, y2)
        rects.append(rect)

    return rects

def read_file(file_name):
    with open (file_name, "r") as file:
        return file.read()

rects = process_input(read_file("input.txt"))
#start_time = time.time()
print calc_total_area(rects)
#end_time = time.time()
#print("--- %s seconds ---" % (end_time - start_time))

"""
def test_total_area():
    print "test 'total_area'"

    rects = [(1, 1, 3, 3),
             (2, 2, 4, 4)]
    assert calc_total_area(rects) == 7
    print "example 1 - success"

    rects = [(1, 1, 7, 7)]
    assert calc_total_area(rects) == 36
    print "example 2 - success"

    rects = []
    assert calc_total_area(rects) == 0
    print "example 3 - sucess"

    rects = [( 0,  0,  6,  5),
             ( 4,  1,  7,  4),
             ( 3,  2,  8,  6),
             (10,  5, 12,  7),
             (11,  6, 13,  8)]
    assert calc_total_area(rects) == 49
    print "example 6 - success"

    rects = [( 6,  8, 14, 15),
             ( 6,  5, 12, 10),
             ( 6,  2, 15, 10),
             ( 6,  7, 14, 14)]
    assert calc_total_area(rects) == 112
    print "example 5 - success"

def test_process_input():
    print "test 'process_input'"

    test_input = "3\n1 2 3 4\n2 3 5 5\n20 30 40 50"
    rects = process_input(test_input)
    assert rects[0] == (1, 2, 3, 4)
    assert rects[1] == (2, 3, 5, 5)
    assert rects[2] == (20, 30, 40, 50)
    print "test process input - success"

    print ""



def test_is_intersected():
    print "test 'is_intersected'"

    r1 = (0, 0, 2, 2)
    r2 = (1, 1, 5, 5)
    assert is_intersected(r1, r2)
    assert is_intersected(r2, r1)
    print "example 1 - success"

    r1 = (0, 1, 3, 5)
    r2 = (1, 0, 5, 3)
    assert is_intersected(r1, r2)
    assert is_intersected(r2, r1)
    print "example 2 - success"

    r1 = (0, 0, 2, 2)
    r2 = (3, 4, 6, 6)
    assert not is_intersected(r1, r2)
    assert not is_intersected(r2, r1)
    print "example 3 (non intersection) - success"

    r1 = (0, 0, 4, 4)
    r2 = (0, 2, 4, 7)
    assert is_intersected(r1, r2)
    assert is_intersected(r2, r1)
    print "example 4 (x matches) - success"

    r1 = (0, 0, 6, 5)
    r2 = (1, 1, 4, 4)
    assert is_intersected(r1, r2)
    assert is_intersected(r2, r1)
    print "example 5 (inner case) success"

    print ""

def test_calc_intersection():
    print "test 'calc_intersection'"

    r1 = (0, 0, 2, 2)
    r2 = (1, 1, 5, 5)
    assert calc_intersection(r1, r2) == (1, 1, 2, 2)
    assert calc_intersection(r2, r1) == (1, 1, 2, 2)
    print "example 1 - success"

    r1 = (0, 1, 3, 5)
    r2 = (1, 0, 5, 3)
    assert calc_intersection(r1, r2) == (1, 1, 3, 3)
    assert calc_intersection(r2, r1) == (1, 1, 3, 3)
    print "example 2 - success"

    r1 = (0, 0, 4, 4)
    r2 = (0, 2, 4, 7)
    assert calc_intersection(r1, r2) == (0, 2, 4, 4)
    assert calc_intersection(r2, r1) == (0, 2, 4, 4)
    print "example 3 (x matches) - success"

    r1 = (0, 0, 6, 5)
    r2 = (1, 1, 4, 4)
    assert calc_intersection(r1, r2) == (1, 1, 4, 4)
    assert calc_intersection(r2, r1) == (1, 1, 4, 4)
    print "example 4 (inner case) success"

    print ""

test_process_input()
test_is_intersected()
test_calc_intersection()
test_total_area() """