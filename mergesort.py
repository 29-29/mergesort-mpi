# March 24, 2025 (Monday)

'''
Topics in Parallel and Distributed Computing:
Introducing Concurrency in Undergraduate Courses
(Edited by Prasad, Gupta, Rosenberg, Sussman, Weems)
Page 56

Figure 3.27 
Parallel mergesort using Pool/map.
The code relies on sequential mergesort from Figure 3.17.
'''

from mpi4py import MPI
import time, random, sys
import numpy as np
# from mergesort_sequential_np import merge, mergesort
from mergesort_sequential_np2 import merge, mergesort

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        N = 500000
        lystbck = np.random.random(N)  # Use NumPy to generate random numbers.

        # Sequential mergesort a copy of the list.
        lyst = np.copy(lystbck)
        start = time.time()
        lyst = mergesort(lyst)
        elapsed = time.time() - start
        print(f'Sequential mergesort: {elapsed} sec')

        # Parallel mergesort.
        lyst = np.copy(lystbck)
        start = time.time()
        lyst = mergeSortParallel(lyst, comm, size)
        elapsed = time.time() - start
        print(f'Parallel mergesort: {elapsed} sec')
    else:
        mergeSortParallel(None, comm, size)

def mergeSortParallel(lyst, comm, size):
    rank = comm.Get_rank()

    if rank == 0:
        numproc = size
        endpoints = np.linspace(0, len(lyst), numproc + 1, dtype=int)
        sublists = [lyst[endpoints[i]:endpoints[i + 1]] for i in range(numproc)]
    else:
        sublists = None

    # Scatter sublists to all processes.
    sublist = comm.scatter(sublists, root=0)

    # Each process sorts its sublist.
    sorted_sublist = mergesort(sublist)

    # Gather sorted sublists back at root.
    gathered = comm.gather(sorted_sublist, root=0)

    if rank == 0:
        # Iteratively merge the sorted sublists.
        while len(gathered) > 1:
            args = [(gathered[i], gathered[i + 1]) for i in range(0, len(gathered), 2)]
            gathered = [merge(a, b) for a, b in args]
        return gathered[0]
    else:
        return None

if __name__ == "__main__":
    main()
