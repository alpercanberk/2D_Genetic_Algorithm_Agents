
import numpy as np
import random
import string

f= open("log.txt","w+")


def rectangle(width, height, type):
    return np.full((width, height), type)

def line_overlap_2d(l1,r1,l2,r2):

    rightmost_index = 2

    if(r1 > r2):
        rightmost_index = 1

    if(rightmost_index == 2):
        if(r1 > l2):
            return True

    if(rightmost_index == 1):
        if(r2 > l1):
            return True

    return False

def does_intersect_2d(x1, y1, width1, height1, x2, y2, width2, height2):
    intersection_type = []
    if(line_overlap_2d(x1, x1+width1, x2, x2+width2) and line_overlap_2d(y1, y1+height1, y2, y2+height2)):
        return True
    return False

def generate_random_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# def parse_log(element):
#     if type(element) == tuple:
#         element = [str.strip(str(e)) for e in element]
#         return ','.join(element)
#     else:
#         return str(element)

def log(*args):
    a = [str(element) for element in args]
    string = ' '.join(a)
    f.write(string + "\n")

def clear_log():
    f.truncate(0)

# print(does_intersect_2d(0,0,10,30,10,10,10,10))
