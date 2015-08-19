#!/usr/bin/env python
# -*- coding: utf-8 -*-
#http://informatics.mccme.ru//mod/statements/view3.php?chapterid=644#1
import sys
import re

x1, y1, x2, y2 = range(4)

def is_intersected(r1, r2):
    return r2[x1] < r1[x2] and r2[y1] < r1[y2] and \
           r2[x2] > r1[x1] and r2[y2] > r1[y1]

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

class Chunks:
    def __init__(self, rects):
        self.rects = rects
        #rect_id_chunks
        self.chunks = [None] * len(rects)
        self.split_to_chunks()

    def split_to_chunks(self):
        rects = self.rects
        n = len(rects)
        for r1_id in xrange(n - 1):
            for r2_id in xrange(r1_id + 1, n):
                    self.update_between(r1_id, r2_id)

    def get_chunks(self):
        return self.chunks

    def update_between(self, r1_id, r2_id):
        chunk = self.get_chunk(r1_id)
        r1, r2 = self.rects[r1_id], self.rects[r2_id]
        if not is_intersected(r1, r2):
            return
        #actuall update
        intersection = calc_intersection(r1, r2)
        chunk.add(intersection)

    def get_chunk(self, rect_id):
        if self.chunks[rect_id] is not None:
            return self.chunks[rect_id]
        return self.create_chunk(rect_id)

    def create_chunk(self, rect_id):
        chunk = set()
        self.chunks[rect_id] = chunk
        return chunk

    def find_chunk(self, rect_id):
        #self.intersecton_chunks[]
        pass

def total_area(rects):
    n = len(rects)
    if n == 0:
        return 0
    if n == 1:
        return calc_area(rects[0])

    raw_area = sum(map(calc_area, rects))
    intr_area = 0

    for r1_id in xrange(n - 1):
        chunk = set()
        for r2_id in xrange(r1_id + 1, n):
            r1, r2 = rects[r1_id], rects[r2_id]
            if is_intersected(r1, r2):
                intersection = calc_intersection(r1, r2)
                chunk.add(intersection)
        intr_area += total_area(list(chunk))

    return raw_area - intr_area

    #chunks = Chunks(rects)
    #intersection_chunks = chunks.get_chunks()

    #intr_area = sum(total_area(list(intr_chunk)) for intr_chunk in intersection_chunks)
    #return raw_area - intr_area

def process_input(input):
    raw_numbers = re.compile('\s+').split(input.strip())
    numbers = map(lambda x: int(float(x)), raw_numbers)
    #num_rects, raw_rects = numbers[0], numbers[1:]
    raw_rects = numbers
    num_rects = len(numbers)/4
    rects = [ tuple(raw_rects[(i * 4):(i * 4 + 4)]) for i in xrange(num_rects)]
    return rects

def read_file(file_name):
    with open (file_name, "r") as file:
        return file.read()

def test_total_area():
    print "test 'total_area'"

    rects = [(1, 1, 3, 3),
             (2, 2, 4, 4)]
    assert total_area(rects) == 7
    print "example 1 - success"

    rects = [(1, 1, 7, 7)]
    assert total_area(rects) == 36
    print "example 2 - success"

    rects = []
    assert total_area(rects) == 0
    print "example 3 - sucess"

    rects = [( 0,  0,  6,  5),
             ( 4,  1,  7,  4),
             ( 3,  2,  8,  6),
             (10,  5, 12,  7),
             (11,  6, 13,  8)]
    assert total_area(rects) == 49

    rects = [( 6,  8, 14, 15),
             ( 6,  5, 12, 10),
             ( 6,  2, 15, 10),
             ( 6,  7, 14, 14)]
    assert total_area(rects) == 112

    print "example 5 - success"

def test_process_input():
    print "test 'process_input'"

    test_input = """
    3
    1 2 3 4
    2 3 5 5
    20 30 40 50
    """
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

rects = process_input(read_file("input.txt"))
#rects = [( 6,  8, 14, 15),
#         ( 6,  5, 12, 10),
#         ( 6,  2, 15, 10),
#         ( 6,  7, 14, 14)]
#print total_area(rects)
#print "should be 112"

#print "example 5 - success"
print total_area(rects)
#test_process_input()
#test_is_intersected()
#test_calc_intersection()
#test_total_area()