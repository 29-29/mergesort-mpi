# March 24, 2025 (Monday)

'''
Topics in Parallel and Distributed Computing:
Introducing Concurrency in Undergraduate Courses
(Edited by Prasad, Gupta, Rosenberg, Sussman, Weems)
Page 46
'''

import numpy as np

def merge(left, right):
    return np.sort(np.concatenate((left, right)))

def mergesort(lyst):
    if len(lyst) <= 1:
        return lyst
    ind = len(lyst) // 2
    return merge(mergesort(lyst[:ind]), mergesort(lyst[ind:]))
